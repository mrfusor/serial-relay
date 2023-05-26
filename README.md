# This is for the cheap usb relay boards that are listed merely as "DC 7V-38V 16 Channel Serial Relay Module USB Relay Switch"
# There is almost no information available on these, but I was able to find a serial code table so I could make this script to send commands to the relays.
# It's pretty self explanitory but there are things that I could improve, I need to add the ability to poll for current state.
# To use, "sudo python relay.py 1 -on" turns relay 1 on, "sudo python relay.py 1 -off" turns it off, substitute the numbers all the way to 16 for the rest. 
# "sudo python relay.py 0 -on" and "sudo python relay.py 0 -off" turn on and off all relays at once.
# For reference, the relay board shows up as: "ID 1a86:7523 QinHeng Electronics HL-340 USB-Serial adapter" with lsusb.
