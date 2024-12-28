import binascii
import argparse
import struct
import serial # pip install pyserial
import time

def open_serial_port(port, baud_rate, bytesize, parity, stopbits, timeout=1):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud_rate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout
        )
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def crouzet_tx_rx(ser, tx):
    print("WRITE:", tx)
    ser.write((":"+tx+"\r\n").encode())
    time.sleep(1)  # Wait for response
    rx1 = ser.read_all().decode()
    if tx.startswith("0103"):
        print("READ:", rx1)
        if rx1.startswith(":010340"):
                # Ignore 7 byte response header and convert to bytes from hexstring
                bytestream = bytes.fromhex(rx1[7:])               
                # Decode the byte bytes 14/15 bytes as little-endian Int16
                pin = struct.unpack('<h', bytestream [13:15])[0]
                print(f"The password is: {pin:04}")
        return
    else:
        print("READ:", rx1)
        return

# Configuration
parser = argparse.ArgumentParser(description='Decode password from Crouzet Millenium 3 device.')
parser.add_argument('serial', help='COM Port of the Millenium 3 USB Cable')
args = parser.parse_args()
port = args.serial
baud_rate = 155200
bytesize = serial.SEVENBITS
parity = serial.PARITY_EVEN
stopbits = serial.STOPBITS_ONE

# Open serial port
ser = open_serial_port(port, baud_rate, bytesize, parity, stopbits)
if not ser:
    print("Failed to open serial port ", port)
    exit

crouzet_tx_rx(ser, "0103000028C040D4")
# it should respond with 
#       READ: :010340
#       READ: 363314010002000202010105005C11000005000000020001000100000000000000000000000FF00000000000000000000000000000000000000000000000005567
# PIN here is 0x5C11, thus the decoded little-endian Int16 value: 4444

# Close serial port
ser.close()