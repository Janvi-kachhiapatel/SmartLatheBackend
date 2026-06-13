from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("10.10.14.132", port=502)

print("Connect =", client.connect())

for unit in [1, 2, 3, 4, 5]:
    try:
        print(f"\nTesting Unit {unit}")

        result = client.read_holding_registers(
            #address=4001,
            count=2,
            device_id=unit
        )

        print(result)

        if hasattr(result, "registers"):
            print("Registers:", result.registers)

    except Exception as e:
        print("ERROR:", e)

client.close()