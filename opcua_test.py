from opcua import Client

url = "opc.tcp://10.10.14.135:4840"
client = Client(url)

try:
    client.connect()
    print("Connected")

    for i in range(0, 17):
        try:
            node = client.get_node(f"ns=4;s=N1_Input_Bit_{i:02d}")
            print(f"N1_Input_Bit_{i:02d} =", node.get_value())
        except:
            pass

    print("\nOUTPUTS\n")

    for i in range(0, 17):
        try:
            node = client.get_node(f"ns=4;s=N2_Output_Bit_{i:02d}")
            print(f"N2_Output_Bit_{i:02d} =", node.get_value())
        except:
            pass

except Exception as e:
    print(e)

finally:
    client.disconnect()