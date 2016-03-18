# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# BH1750_driver.py - the core code to read illuminance from BH1750.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import time
import smbus

# BH1750 i2c address
addr = 0x23
# debug flag
debug = False

def bh1750_read():
	bus = smbus.SMBus(1)
	data = bus.read_i2c_block_data(addr,0x11)
	illu = round((data[1] + (256 * data[0])) / 1.2,2)
	if debug:
		print "illuminance = %.2f lx" %illu
	return {'illuminance' : illu}
