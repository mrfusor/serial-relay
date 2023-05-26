#!/usr/bin/env python3
import sys
import usb.core
import usb.util
import time

# Parse command-line arguments
if len(sys.argv) != 3:
    print("Usage: python relay.py <relay number> <-on/-off>")
    sys.exit(1)

relay_number = int(sys.argv[1])
command = sys.argv[2]

if relay_number < 0 or relay_number > 16:
    print("Invalid relay number. Please enter a number between 1 and 16.")
    sys.exit(1)

if command not in ["-on", "-off"]:
    print("Invalid command. Please use -on to turn the relay on, or -off to turn it off.")
    sys.exit(1)

# Define commands for each relay
relay_commands = {
    1: {"-on": "3A 46 45 30 35 30 30 30 30 46 46 30 30 46 45 0D 0A", "-off": "3A 46 45 30 35 30 30 30 30 30 30 30 30 46 44 0D 0A"},
    2: {"-on": "3A 46 45 30 35 30 30 30 31 46 46 30 30 46 44 0D 0A", "-off": "3A 46 45 30 35 30 30 30 31 30 30 30 30 46 43 0D 0A"},
    3: {"-on": "3A 46 45 30 35 30 30 30 32 46 46 30 30 46 43 0D 0A", "-off": "3A 46 45 30 35 30 30 30 32 30 30 30 30 46 42 0D 0A"},
    4: {"-on": "3A 46 45 30 35 30 30 30 33 46 46 30 30 46 42 0D 0A", "-off": "3A 46 45 30 35 30 30 30 33 30 30 30 30 46 41 0D 0A"},
    5: {"-on": "3A 46 45 30 35 30 30 30 34 46 46 30 30 46 41 0D 0A", "-off": "3A 46 45 30 35 30 30 30 34 30 30 30 30 46 39 0D 0A"},
    6: {"-on": "3A 46 45 30 35 30 30 30 35 46 46 30 30 46 39 0D 0A", "-off": "3A 46 45 30 35 30 30 30 35 30 30 30 30 46 38 0D 0A"},
    7: {"-on": "3A 46 45 30 35 30 30 30 36 46 46 30 30 46 38 0D 0A", "-off": "3A 46 45 30 35 30 30 30 36 30 30 30 30 46 37 0D 0A"},
    8: {"-on": "3A 46 45 30 35 30 30 30 37 46 46 30 30 46 37 0D 0A", "-off": "3A 46 45 30 35 30 30 30 37 30 30 30 30 46 36 0D 0A"},
    9: {"-on": "3A 46 45 30 35 30 30 30 38 46 46 30 30 46 36 0D 0A", "-off": "3A 46 45 30 35 30 30 30 38 30 30 30 30 46 35 0D 0A"},
    10: {"-on": "3A 46 45 30 35 30 30 30 39 46 46 30 30 46 35 0D 0A", "-off": "3A 46 45 30 35 30 30 30 39 30 30 30 30 46 34 0D 0A"},
    11: {"-on": "3A 46 45 30 35 30 30 30 41 46 46 30 30 46 34 0D 0A", "-off": "3A 46 45 30 35 30 30 30 41 30 30 30 30 46 33 0D 0A"},
    12: {"-on": "3A 46 45 30 35 30 30 30 42 46 46 30 30 46 33 0D 0A", "-off": "3A 46 45 30 35 30 30 30 42 30 30 30 30 46 32 0D 0A"},
    13: {"-on": "3A 46 45 30 35 30 30 30 43 46 46 30 30 46 32 0D 0A", "-off": "3A 46 45 30 35 30 30 30 43 30 30 30 30 46 31 0D 0A"},
    14: {"-on": "3A 46 45 30 35 30 30 30 44 46 46 30 30 46 31 0D 0A", "-off": "3A 46 45 30 35 30 30 30 44 30 30 30 30 46 30 0D 0A"},
    15: {"-on": "3A 46 45 30 35 30 30 30 45 46 46 30 30 46 30 0D 0A", "-off": "3A 46 45 30 35 30 30 30 45 30 30 30 30 46 46 0D 0A"},
    16: {"-on": "3A 46 45 30 35 30 30 30 46 46 46 30 30 46 46 0D 0A", "-off": "3A 46 45 30 35 30 30 30 46 30 30 30 30 46 45 0D 0A"},
    0: {"-on": "3A 46 45 30 46 30 30 30 30 30 30 31 30 30 32 46 46 46 46 45 33 0D 0A", "-off": "3A 46 45 30 46 30 30 30 30 30 30 31 30 30 32 30 30 30 30 45 31 0D 0A"},

}

# Find USB device
dev = usb.core.find(idVendor=0x1a86, idProduct=0x7523)

if dev is None:
    raise ValueError('Device not found')

# Detach kernel driver if active
reattach = False
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)

# Set the default configuration
dev.set_configuration()

# Get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# Convert the command to a byte array
command_bytes = bytes.fromhex(relay_commands[relay_number][command].replace(" ", ""))

# Send the command
ep.write(command_bytes)

# Reattach kernel driver if necessary
if reattach:
    dev.attach_kernel_driver(0)

