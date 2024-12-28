# Crouzet Password Recovery
Tooling to recover your lost password for protected programs on Crouzet Millenium 3 PLCs (XD26, XD10, etc)

# Purpose
You might have programmed your PLC a long time ago and have for some reason protected it against reading or monitoring using the password protection provided by Crouzet's "M3 soft". It allows you to set a four-digit "password" when uploading you program to the PLC. This little hack allows you to recover that password in no time.

# Usage
Connect your Serial Cable to the PLC and your Laptop. Check Device Manager which COM-Port is assigned to the Crouzet Millenium 3 Serial adaptor-cable and run this tool with the COM-Port as an argument:

```
py Get_Crouzet_PIN.py COM3
```

I'm using the USB-Version of the serial cable, but any variant should do. If you don't want to spend 50 euros on Ebay for this, you could build your own. See [Bootsale Haul - SSR's and Crouzet Millenium 3 PLC - DIY Programming](https://youtu.be/k1yhU4jOdg8?t=680) for a DIY-variant that should work as well.

# Background
Using serial port sniffing, you can easily spot that the connection uses 115.200 baud and 7E1 serial settings. The protocol used by the PLC uses ASCII-encoded hex sequences. Commands sent typically start with ":01" and end with "\r\n". They are answered by the PLC with a paired 3-byte response header also starting with ":01" and a longer payload (typically 132 bytes, also ending with "\r\n"). 
When you try to download a protected program, the protocol will be followed through (about 20 request/response steps) until you will need to enter the "password".
You have five tries before a 30 minute password lock prolongs any brute force attacks.
The "password" is validated client side in M3 soft, not the PLC! For this the INT16 little-endian value of the numberic "password" is send to the M3 soft to have it check your password input.
All that is needed is to send this particualy request and decode password send to M3 soft.

Have fun with PLC programming!

# Prerequisites
- Python for windows
- pyserial 
- serial cable
- I see no reason why it shouldn't work on mac or linux

# Tooling for further procotcol analysis
- PortMon works on 32-bit windows only
- M3 soft
- Windows 10 worked well for both
- Winn10 provides generic serial drivers, but M3 soft will bring their own
