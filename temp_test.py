# from pymodbus.client import ModbusTcpClient

# client = ModbusTcpClient(
#     "10.10.14.127",
#     port=502
# )

# print("Connect =", client.connect())

# for addr in [4001, 4003, 4031, 4035]:

#     print(f"\nTesting Register {addr}")

#     try:

#         result = client.read_holding_registers(
#             address=addr,
#             count=2,
#             device_id=2
#         )

#         print(result)

#         if hasattr(result, "registers"):
#             print("Registers =", result.registers)

#     except Exception as e:
#         print("ERROR =", e)

# client.close()
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

exit()