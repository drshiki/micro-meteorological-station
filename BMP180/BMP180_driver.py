import time
import smbus
 
#i2c address.
i2c_addr = 0x77

#simple mode
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


addr_ctrl= 0xF4

addr_data_temp = 0xF6
addr_data_press = 0xF6


cmd_read_temp = 0x2E
cmd_read_press = 0x34
 
data_AC1 = 0
data_AC2 =    0
data_AC3 = 0
data_AC4 = 0
data_AC5 = 0
data_AC6 = 0
data_B1  = 0
data_B2  = 0
data_MB  = 0
data_MC  = 0
data_MD  = 0

#-----------------------------------------------
mode = mode_standard;
address = i2c_addr;
bus = smbus.SMBus(1)

def bmp180_read():
	read_calibration();
	temp = read_temperature();
	press = read_pressure();
	
	return [temp, press];
	
def read_byte(cmd):
	return bus.read_byte_data(address,cmd)


def read_u16(cmd):

	MSB = bus.read_byte_data(address,cmd)
	LSB = bus.read_byte_data(address,cmd+1)

	return (MSB << 8) + LSB
 
def read_s16(cmd):
	result = read_u16(cmd)
	if result > 32767:
		result -= 65536

	return result

def write_byte(cmd,val):
	bus.write_byte_data(address,cmd,val)

def read_calibration():
	global data_AC1;
	global data_AC2;
	global data_AC3;
	global data_AC4;
	global data_AC5;
	global data_AC6;
	global data_B1;
	global data_B2;
	global data_MB;
	global data_MC;
	global data_MD;
	data_AC1 = read_s16(addr_AC1)   # INT16
	data_AC2 = read_s16(addr_AC2)   # INT16
	data_AC3 = read_s16(addr_AC3)   # INT16
	data_AC4 = read_u16(addr_AC4)   # UINT16
	data_AC5 = read_u16(addr_AC5)   # UINT16
	data_AC6 = read_u16(addr_AC6)   # UINT16
	data_B1  = read_s16(addr_B1)     # INT16
	data_B2  = read_s16(addr_B2)     # INT16
	data_MB  = read_s16(addr_MB)     # INT16
	data_MC  = read_s16(addr_MC)     # INT16
	data_MD  = read_s16(addr_MD)     # INT16

def read_raw_temp():
	write_byte(addr_ctrl, cmd_read_temp)
	time.sleep(0.005)  # Wait 5ms
	MSB = read_byte(addr_data_temp)
	LSB = read_byte(addr_data_temp+1)
	raw = (MSB << 8) + LSB
	return raw

def read_raw_pressure():
	write_byte(addr_ctrl, cmd_read_press + (mode << 6))
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
	UT = read_raw_temp()
	X1 = ((UT - data_AC6) * data_AC5) >> 15
	X2 = (data_MC << 11) / (X1 + data_MD)
	B5 = X1 + X2
	temp = ((B5 + 8) >> 4) / 10.0
	
	return temp

def read_pressure():

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

# Calculation taken straight from section 3.6 of the datasheet.

	pressure = float(read_pressure())

	altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))

	return altitude

def read_sealevel_pressure(altitude_m=0.0):
	pressure = float(read_pressure())
	p0 = pressure / pow(1.0 - altitude_m/44330.0, 5.255)

	return p0


