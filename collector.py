from datetime import datetime
import struct
from pymodbus.client import ModbusTcpClient
from opcua import Client as OPCClient
import requests

MODBUS_HOST = "10.10.14.127"
MODBUS_PORT = 502

OPCUA_URL = "opc.tcp://10.10.14.135:4840"
ESP32_URL = "http://10.10.14.131/data"


def decode_float_vibit(registers):
    try:
        if not registers or len(registers) < 2:
            return 0.0

        packed = struct.pack(">HH", registers[1], registers[0])
        return round(struct.unpack(">f", packed)[0], 2)

    except:
        return 0.0


def decode_float_energy(registers):
    try:
        if not registers or len(registers) < 2:
            return 0.0

        packed = struct.pack(">HH", registers[0], registers[1])
        return round(struct.unpack(">f", packed)[0], 2)

    except:
        return 0.0


def decode_int(registers):
    try:
        if not registers:
            return 0
        return int(registers[0] & 0xFFFF)
    except:
        return 0


def safe_read(client, unit, address, count=2):
    print("SAFE_READ CALLED", unit, address)

    try:
        result = client.read_holding_registers(
            address=address,
            count=count,
            device_id=unit
        )

        print("RESULT =", result)

        if result.isError():
            print("MODBUS ERROR =", result)
            return []

        print("REGISTERS =", result.registers)

        return result.registers

    except Exception as e:
        print("MODBUS EXCEPTION =", e)
        return []
        print("REGISTERS =", result.registers)

def read_vibit(client, unit):
    return {
        #"x_rms_acceleration": decode_float_vibit(safe_read(client, unit, 4001)),
        "y_rms_acceleration": decode_float_vibit(safe_read(client, unit, 4003)),
        "z_rms_acceleration": decode_float_vibit(safe_read(client, unit, 4005)),

        "x_rms_velocity": decode_float_vibit(safe_read(client, unit, 4007)),
        "y_rms_velocity": decode_float_vibit(safe_read(client, unit, 4009)),
        "z_rms_velocity": decode_float_vibit(safe_read(client, unit, 4011)),

        "temperature": decode_float_vibit(safe_read(client, unit, 4013)),

        "x_peak_acceleration": decode_float_vibit(safe_read(client, unit, 4015)),
        "y_peak_acceleration": decode_float_vibit(safe_read(client, unit, 4017)),
        "z_peak_acceleration": decode_float_vibit(safe_read(client, unit, 4019)),

        "x_peak_velocity": decode_float_vibit(safe_read(client, unit, 4021)),
        "y_peak_velocity": decode_float_vibit(safe_read(client, unit, 4023)),
        "z_peak_velocity": decode_float_vibit(safe_read(client, unit, 4025)),

        #"reboot_count": decode_int(safe_read(client, unit, 4031, 1)),
        #"led_status": decode_int(safe_read(client, unit, 4035, 1)),

        "rpm": 0
    }


def read_energy(client):
    def read_input(addr):
        try:
            result = client.read_input_registers(
                address=addr,
                count=2,
                device_id=3
            )

            if result.isError():
                return 0

            return decode_float_energy(result.registers)

        except:
            return 0

    return {
        "voltage_V1N": read_input(0),
        "voltage_V2N": read_input(2),
        "voltage_V3N": read_input(4),
        "avg_voltage_LN": read_input(6),

        "voltage_V12": read_input(8),
        "voltage_V23": read_input(10),
        "voltage_V31": read_input(12),
        "avg_voltage_LL": read_input(14),

        "current_I1": read_input(16),
        "current_I2": read_input(18),
        "current_I3": read_input(20),
        "avg_current": read_input(22),

        "kW1": read_input(24),
        "kW2": read_input(26),
        "kW3": read_input(28),
        "total_kW": read_input(42),

        "PF1": read_input(48),
        "PF2": read_input(50),
        "PF3": read_input(52),
        "avg_PF": read_input(54),

       "frequency": read_input(56),

        # Additional Parameters found in Node-RED
        "total_net_kwh_dg": read_input(64),
        "total_net_kvarh_dg": read_input(66),
        "total_net_kvah_dg": read_input(68),

        "max_dmd_active_power": read_input(70),
        "max_dmd_reactive_power": read_input(72),
        "max_dmd_apparent_power": read_input(74),

        "kwh1_import": read_input(76),
        "kwh2_import": read_input(78),
        "kwh3_import": read_input(80),

        "kwh1_export": read_input(82),
        "kwh2_export": read_input(84),
        "kwh3_export": read_input(86),

        "total_kwh_import": read_input(88),
        "total_kwh_export": read_input(90),

        "kvarh1_import": read_input(92),

        "kVA1": read_input(64),
        "kVA2": read_input(66),
        "kVA3": read_input(68),

        "kVAR1": read_input(70),
        "kVAR2": read_input(72),
        "kVAR3": read_input(74),

        "kvar1": read_input(30),
        "kvar2": read_input(32),
        "kvar3": read_input(34),

        "kva1": read_input(36),
        "kva2": read_input(38),
        "kva3": read_input(40),

        "total_kw": read_input(42),
        "total_kvar": read_input(44),
        "total_kva": read_input(46),

        # "pf1": read_input(48),
        # "pf2": read_input(50),
        # "pf3": read_input(52),
        # "avg_pf": read_input(54),

        "total_net_kwh": read_input(58),
        "total_net_kvarh": read_input(60),
        }


def read_opc():
    machine_status = "OFF"
    position = {
        "x_position": 0,
        "y_position": 0,
        "cutting_speed": 0,
        "depth_of_cutting": 0
    }

    chuck = {
        "chuck_on": 0,
        "red_buzzer": 0
    }

    opc = OPCClient(OPCUA_URL)

    try:
        opc.connect()

        machine_status = "ON"

        chuck_node = opc.get_node("ns=4;s=N2_Output_Bit_04")
        chuck["chuck_on"] = 1 if chuck_node.get_value() else 0

    except:
        machine_status = "OFF"

    finally:
        try:
            opc.disconnect()
        except:
            pass

    return machine_status, position, chuck

def read_esp32():
    try:
        response = requests.get(
            ESP32_URL,
            timeout=2
        )

        data = response.json()

        return {
      "machine_status": data.get("machine_status", "OFF"),
    "chuck_key_status": data.get("chuck_key_status", 0),
    "red_buzzer": data.get("red_buzzer", 0),

    "x_position": data.get("x_position", 0),
    "y_position": data.get("y_position", 0),

    "rpm": data.get("rpm", 0),
    "depth_of_cutting": data.get("depth_of_cutting", 0),
    "cutting_speed": data.get("cutting_speed", 0),
}

    except Exception as e:
        print("ESP32 Error:", e)

        return {
            "x_position": 0,
            "y_position": 0,
            "rpm": 0,
            "depth_of_cutting": 0,
            "cutting_speed": 0,
        }

def collect_live_data():

    vibit1 = {
        "temperature": 0,
        "rpm": 0
    }

    vibit2 = {
        "temperature": 0,
        "rpm": 0
    }

    energy = {}

    print("===== COLLECT LIVE DATA CALLED =====")
    print("BEFORE CLIENT.CONNECT")
    print("MODBUS HOST =", MODBUS_HOST)

    client = ModbusTcpClient(
        MODBUS_HOST,
        port=MODBUS_PORT
    )

    if client.connect():
        print("MODBUS CONNECTED")

        vibit1 = read_vibit(client, 1)
        vibit2 = read_vibit(client, 2)
        energy = read_energy(client)

        client.close()

    else:
        print("MODBUS CONNECTION FAILED")

    machine_status, position, chuck = read_opc()

    esp32 = read_esp32()
    print("ESP DATA =", esp32)

    
    # Position
    position["x_position"] = esp32["x_position"]
    position["y_position"] = esp32["y_position"]
    position["depth_of_cutting"] = esp32["depth_of_cutting"]
    position["cutting_speed"] = esp32["cutting_speed"]

    # RPM
    rpm_value = esp32["rpm"]

    # Machine status from ESP
    machine_status = esp32["machine_status"]

    # Chuck from ESP
    chuck["chuck_on"] = esp32["chuck_key_status"]
    chuck["red_buzzer"] = esp32["red_buzzer"]

    vibit1["rpm"] = rpm_value
    vibit2["rpm"] = rpm_value

    return {
        "machine": {
            "status": machine_status,
            "timestamp": datetime.utcnow().isoformat()
        },

        "vibit1": vibit1,
        "vibit2": vibit2,

        "energy": {
            "timestamp": datetime.utcnow().isoformat(),
            "completeness": "complete",
            "data": energy,
            "schema_version": "3.0"
        },

        "position": position,
        "chuck": chuck
    }

    machine_status, position, chuck = read_opc()

    esp32 = read_esp32()
    print("ESP DATA =", esp32)

    position["x_position"] = esp32["x_position"]
    position["y_position"] = esp32["y_position"]

    rpm_value = esp32["rpm"]

    vibit1["rpm"] = rpm_value
    vibit2["rpm"] = rpm_value

    return {
        "machine": {
            "status": machine_status,
            "timestamp": datetime.utcnow().isoformat()
        },

        "vibit1": vibit1,
        "vibit2": vibit2,

        "energy": {
            "timestamp": datetime.utcnow().isoformat(),
            "completeness": "complete",
            "data": energy,
            "schema_version": "3.0"
        },

        "position": position,
        "chuck": chuck
    }