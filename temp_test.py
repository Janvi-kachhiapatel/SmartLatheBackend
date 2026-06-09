from pymodbus.client import ModbusTcpClient
import struct

def decode(regs):
    packed = struct.pack(">HH", regs[0], regs[1])
    return round(struct.unpack(">f", packed)[0], 4)

client = ModbusTcpClient("10.10.14.127", port=502)

if client.connect():

    for addr in range(56, 80, 2):

        r = client.read_input_registers(
            address=addr,
            count=2,
            device_id=3
        )

        if not r.isError():
            print(f"{addr} = {decode(r.registers)}")

    client.close()