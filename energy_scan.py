from pymodbus.client import ModbusTcpClient
import struct

HOST = "10.10.14.127"
PORT = 502

UNIT_IDS = [1, 2, 3, 4, 5]


def decode_float_vibit(registers):
    try:
        packed = struct.pack(">HH", registers[1], registers[0])
        return round(struct.unpack(">f", packed)[0], 2)
    except:
        return None


client = ModbusTcpClient(HOST, port=PORT)

if client.connect():
    print("Connected\n")

    for unit in UNIT_IDS:
        print(f"\n===== UNIT {unit} =====")

        for addr in [3000, 3002, 3004, 3016, 3022, 3048]:
            try:
                result = client.read_input_registers(
                    address=addr,
                    count=2,
                    device_id=unit
                )

                if not result.isError():
                    value = decode_float_vibit(result.registers)
                    print(f"Addr {addr} = {value}")

            except:
                pass

    client.close()

else:
    print("Connection failed")