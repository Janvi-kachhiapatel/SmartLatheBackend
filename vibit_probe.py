from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("10.10.14.127", port=502)

print("Connect =", client.connect())

for unit in [1, 2, 3, 4, 5, 10]:
    try:
        print(f"\nUNIT {unit}")

        result = client.read_input_registers(
            address=12,
            count=2,
            device_id=unit
        )

        print(result)

        if hasattr(result, "registers"):
            print("REGISTERS =", result.registers)

    except Exception as e:
        print("ERROR =", e)

client.close()