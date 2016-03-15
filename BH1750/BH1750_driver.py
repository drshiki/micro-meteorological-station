import time;
import smbus;

addr = 0x23;
debug = True;

def bh1750_read():
	bus = smbus.SMBus(1)
	data = bus.read_i2c_block_data(addr,0x11)
	light = round((data[1] + (256 * data[0])) / 1.2,2);
	if debug == True:
		print "light intensity = %.2f lx"%light;
	return light;
