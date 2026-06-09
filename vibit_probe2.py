from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("10.10.14.127", port=502)

print("Connect =", client.connect())

for addr in [4011, 4013, 4039]:
    try:
        print(f"\nADDRESS {addr}")

        result = client.read_holding_registers(
            address=addr,
            count=2,
            device_id=1
        )

        print(result)

        if hasattr(result, "registers"):
            print(result.registers)

    except Exception as e:
        print("ERROR =", e)

client.close()