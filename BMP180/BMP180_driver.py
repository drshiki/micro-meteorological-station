# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# BMP180_driver.py - the core code to read temperature and pressure from BMP180.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import time
import smbus

# i2c address
i2c_addr = 0x77

# simple mode
mode_ultralower = 0
mode_standard = 1
mode_highers = 2
mode_ultrahighers = 3

# register address
addr_AC1 = 0xAA
addr_AC2 = 0xAC
addr_AC3 = 0xAE
addr_AC4 = 0xB0
addr_AC5 = 0xB2
addr_AC6 = 0xB4
addr_B1 = 0xB6
addr_B2 = 0xB8
addr_MB = 0xBA
addr_MC = 0xBC
addr_MD = 0xBE

# operation code address
addr_ctrl= 0xF4

# data address
addr_data_temp = 0xF6
addr_data_press = 0xF6

# operation code
cmd_read_temp = 0x2E
cmd_read_press = 0x34

# calibration bit
data_AC1 = 0
data_AC2 = 0
data_AC3 = 0
data_AC4 = 0
data_AC5 = 0
data_AC6 = 0
data_B1 = 0
data_B2 = 0
data_MB = 0
data_MC = 0
data_MD = 0

# set parameters for this program
mode = mode_standard
address = i2c_addr
bus = smbus.SMBus(1)

def bmp180_read():
	"""the interface to get the return of temperature and pressure"""
	read_calibration()
	temp = read_temperature()
	press = read_pressure()
	alti = read_altitude()
	s_press = read_sealevel_pressure()
	return [temp, press, alti, s_press]
	
def read_byte(cmd):
	return bus.read_byte_data(address, cmd)

def write_byte(cmd, val):
	bus.write_byte_data(address, cmd, val)

def read_u16(cmd):
	"""read 16 bit unsigned integer"""
	MSB = bus.read_byte_data(address, cmd)
	LSB = bus.read_byte_data(address, cmd+1)
	return (MSB << 8) + LSB
 
def read_s16(cmd):
	"""read 16 bit signed integer"""
	result = read_u16(cmd)
	if result > 32767:
		result -= 65536
	return result

def read_calibration():
	"""get each calibration bit"""
	# modify the value of global variables
	global data_AC1
	global data_AC2
	global data_AC3
	global data_AC4
	global data_AC5
	global data_AC6
	global data_B1
	global data_B2
	global data_MB
	global data_MC
	global data_MD
	data_AC1 = read_s16(addr_AC1)
	data_AC2 = read_s16(addr_AC2)
	data_AC3 = read_s16(addr_AC3)
	data_AC4 = read_u16(addr_AC4)
	data_AC5 = read_u16(addr_AC5)
	data_AC6 = read_u16(addr_AC6)
	data_B1 = read_s16(addr_B1)
	data_B2 = read_s16(addr_B2)
	data_MB = read_s16(addr_MB)
	data_MC = read_s16(addr_MC)
	data_MD = read_s16(addr_MD)

def read_raw_temp():
	# write the operate code to read temperature
	write_byte(addr_ctrl, cmd_read_temp)
	time.sleep(0.005)  # delay for 5ms
	MSB = read_byte(addr_data_temp)
	LSB = read_byte(addr_data_temp+1)
	raw = (MSB << 8) + LSB
	return raw

def read_raw_pressure():
	# write the operate code to read pressure
	write_byte(addr_ctrl, cmd_read_press+(mode<<6))
	if mode == mode_ultralower:
		time.sleep(0.005)
	elif mode == mode_highers:
		time.sleep(0.014)
	elif mode == mode_ultrahighers:
		time.sleep(0.026)
	else:
		time.sleep(0.008)
	MSB = read_byte(addr_data_press)
	LSB = read_byte(addr_data_press+1)
	XLSB = read_byte(addr_data_press+2)
	raw = ((MSB << 16) + (LSB << 8) + XLSB) >> (8 - mode)
	return raw

def read_temperature():
	"""calculate the true temperature in celsius"""
	UT = read_raw_temp()
	X1 = ((UT - data_AC6) * data_AC5) >> 15
	X2 = (data_MC << 11) / (X1 + data_MD)
	B5 = X1 + X2
	temp = ((B5 + 8) >> 4) / 10.0
	return temp

def read_pressure():
	"""calculate the true pressure in Pa"""
	UT = read_raw_temp()
	UP = read_raw_pressure()
	X1 = ((UT - data_AC6) * data_AC5) >> 15
	X2 = (data_MC << 11) / (X1 + data_MD)
	B5 = X1 + X2
	B6 = B5 - 4000
	X1 = (data_B2 * (B6 * B6) >> 12) >> 11
	X2 = (data_AC2 * B6) >> 11
	X3 = X1 + X2
	B3 = (((data_AC1 * 4 + X3) << mode) + 2) / 4
	X1 = (data_AC3 * B6) >> 13
	X2 = (data_B1 * ((B6 * B6) >> 12)) >> 16
	X3 = ((X1 + X2) + 2) >> 2
	B4 = (data_AC4 * (X3 + 32768)) >> 15
	B7 = (UP - B3) * (50000 >> mode)
	if B7 < 0x80000000:
		p = (B7 * 2) / B4
	else:
		p = (B7 / B4) * 2
	X1 = (p >> 8) * (p >> 8)
	X1 = (X1 * 3038) >> 16
	X2 = (-7357 * p) >> 16
	p = p + ((X1 + X2 + 3791) >> 4)
	return p

def read_altitude(sealevel_pa=101325.0):
	pressure = float(read_pressure())
	altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))
	return altitude

def read_sealevel_pressure(altitude_m=0.0):
	pressure = float(read_pressure())
	s_press = pressure / pow(1.0 - altitude_m/44330.0, 5.255)
	return s_press