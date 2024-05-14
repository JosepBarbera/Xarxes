import pyshark
import nest_asyncio

nest_asyncio.apply()

handshake_messages = pyshark.FileCapture(input_file="tradio.pcapng",display_filter='EAPOL')


for packet in handshake_messages:
   print("Source IP:", packet.ip.src)

