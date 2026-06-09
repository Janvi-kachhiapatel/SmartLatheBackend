from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient(
    host="10.10.14.127",
    port=502,
    timeout=10
)

print("Connected =", client.connect())

try:
    result = client.read_input_registers(
        address=0,
        count=2,
        device_id=1
    )

    print(result)

except Exception as e:
    print("ERROR:", e)

client.close()