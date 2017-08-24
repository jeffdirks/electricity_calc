#!/usr/bin/python3

import smbus
import time
import datetime
import sys
import csv

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
read_times = int(input("How many times should the circuit be checked? "))

# seconds to wait between each reading
wait_time = int(input("What is the interval in seconds between each check? "))

# voltage of the circuit
voltage = int(input("What is the voltage of the circuit? "))

# file name to store the data
file_name = input("What should the filename be where the data is stored? ")

with open(file_name, "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    for x in range(0, read_times):
        print(x)
        ts = datetime.datetime.now()
        print(ts)
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
            writer.writerow([ts, amps, watts])
            print("Wrote data to file.")
            time.sleep(wait_time)

        # kept having errors with either reading or writing the data
        # this error handling just skips that attempt at reading the data
        # and continues on to the next one.
        except IOError:
            print("Error reading or writing to the bus.")
