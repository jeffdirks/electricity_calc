#!/usr/bin/python3

import smbus
import time
import sys

# Get I2C bus

bus = smbus.SMBus(1)

# number of channels the monitoring board has
no_of_channels = 1

# PECMAC125A address, 0x2A(42)
# Command for reading current
# 0x6A(106), 0x01(1), 0x01(1),0x0C(12), 0x00(0), 0x00(0) 0x0A(10)
# Header byte-2, command-1, start channel-1, stop channel-12, byte 5 and 6 reserved, checksum
# ControlEverying.com has a Current Monitoring Reference Guide on their website
# for the board. Instructions are there on how to calculate the checksum
read_power_flow_command = [0x6A, 0x01, 0x01, 0x00, 0x00, 0xFF]

# number of times to read the current
read_times = 10

# seconds to wait between each reading
wait_time = 15

# voltage of the circuit
voltage = 220

for x in range(0, read_times):
    print(x)
    try:
        bus.write_i2c_block_data(0x2A, 0x92, read_power_flow_command)
        time.sleep(0.5)
        data = bus.read_i2c_block_data(0x2A, 0x55, 4)

        # convert the data
        msb1 = data[0]
        msb = data[1]
        lsb = data[2]

        amps = (msb1 * 65536 + msb * 256 + lsb) / 1000.0
        watts = amps * voltage

        print("Current amps : %.3f A" %amps)
        print("Current watts : %.3f w" %watts)
        time.sleep(wait_time)

    # kept having errors with either reading or writing the data
    # this error handling just skips that attempt at reading the data
    # and continues on to the next one.
    except IOError:
        print("Error reading or writing to the bus.")
