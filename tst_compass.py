#!/usr/bin/python

import smbus
import time
import numpy as np


def merge(lower_byte, higher_byte):
    """merge 2 bytes (2*8 bits) to form a 16-bit long binary integer"""
    higher_byte << 8  # 8-bit shift
    res = bin(lower_byte | higher_byte)  # sum of low and high bytes
    return res


def bin2decs(C):
    """Convert a binary string into a signed decimal integer"""
    if C[0] == "0":
        # if the first character is '0', the result will be positive
        return int(C, 2)
    else:
        # if the first character is '1', the result will be negative
        return int(C, 2)-(1 << len(C))


def convert(tab):
    """ convert a table of 6 bytes into 3 decimal integers"""
    three_values = [0, 0, 0]
    for i in range(0, 6, 2):
        two_bytes = merge(six_values[i], six_values[i+1])
        str_two_bytes = str(two_bytes)
        three_values[int(i/2)] = bin2decs(str_two_bytes)
    return three_values


def write(tab):
    fichier.write("\n"+str(tab[0])+";"+str(tab[1])+";"+str(tab[2])+";")


if __name__ == "__main__":
    # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
    bus = smbus.SMBus(1)

    # 7 bit address (will be left shifted to add the read write bit)
    DEVICE_ADDRESS = 0x1e
    CTRL_REG3 = 0x22
    OUT_X_L = 0x28  # first data register to read

    # Write a single register
    # Set continuous-conversion mode to (MD1=0,MD0=0)
    bus.write_byte_data(DEVICE_ADDRESS, CTRL_REG3, 0b00000000)

    # Read an array of registers
    six_values = [0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
    three_values = [0, 0, 0]
    dt = 1
    fichier = open("data_compass.csv", "w")
    for t in range(1000):
        six_values = bus.read_i2c_block_data(DEVICE_ADDRESS, OUT_X_L, 6)
        # print(six_values)
        three_values = convert(six_values)
        write(three_values)
        time.sleep(dt)
    fichier.close()