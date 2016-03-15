import time

import smbus
 
# BMP085 default address.

BMP180_I2CADDR           = 0x77
	 
# Operating Modes

BMP180_ULTRALOWPOWER     = 0

BMP180_STANDARD          = 1

BMP180_HIGHRES           = 2

BMP180_ULTRAHIGHRES      = 3
	 

# BMP085 Registers

BMP180_CAL_AC1           = 0xAA  # R   Calibration data (16 bits)
	
BMP180_CAL_AC2           = 0xAC  # R   Calibration data (16 bits)

BMP180_CAL_AC3           = 0xAE  # R   Calibration data (16 bits)

BMP180_CAL_AC4           = 0xB0  # R   Calibration data (16 bits)

BMP180_CAL_AC5           = 0xB2  # R   Calibration data (16 bits)

BMP180_CAL_AC6           = 0xB4  # R   Calibration data (16 bits)
		

BMP180_CAL_B1            = 0xB6  # R   Calibration data (16 bits)

BMP180_CAL_B2            = 0xB8  # R   Calibration data (16 bits)

BMP180_CAL_MB            = 0xBA  # R   Calibration data (16 bits)

BMP180_CAL_MC            = 0xBC  # R   Calibration data (16 bits)

BMP180_CAL_MD            = 0xBE  # R   Calibration data (16 bits)

BMP180_CONTROL           = 0xF4

BMP180_TEMPDATA          = 0xF6

BMP180_PRESSUREDATA      = 0xF6


# Commands

BMP180_READTEMPCMD       = 0x2E

BMP180_READPRESSURECMD   = 0x34
	 
class BMP180(object):

	def __init__(self, address=BMP180_I2CADDR, mode=BMP180_STANDARD):

		self._mode = mode

		self._address = address

		self._bus = smbus.SMBus(1)

		# Load calibration values.

		self._load_calibration()

	def _read_byte(self,cmd):

		return self._bus.read_byte_data(self._address,cmd)

	 

	def _read_u16(self,cmd):

		MSB = self._bus.read_byte_data(self._address,cmd)

		LSB = self._bus.read_byte_data(self._address,cmd+1)

		return (MSB << 8) + LSB
	 
	def _read_s16(self,cmd):

		result = self._read_u16(cmd)

		if result > 32767:result -= 65536

		return result

	 

	def _write_byte(self,cmd,val):

		self._bus.write_byte_data(self._address,cmd,val)

	def _load_calibration(self):
		"load calibration"

		self.cal_AC1 = self._read_s16(BMP180_CAL_AC1)   # INT16
		self.cal_AC2 = self._read_s16(BMP180_CAL_AC2)   # INT16
		self.cal_AC3 = self._read_s16(BMP180_CAL_AC3)   # INT16
		self.cal_AC4 = self._read_u16(BMP180_CAL_AC4)   # UINT16
		self.cal_AC5 = self._read_u16(BMP180_CAL_AC5)   # UINT16
		self.cal_AC6 = self._read_u16(BMP180_CAL_AC6)   # UINT16
		self.cal_B1  = self._read_s16(BMP180_CAL_B1)     # INT16
		self.cal_B2  = self._read_s16(BMP180_CAL_B2)     # INT16
		self.cal_MB  = self._read_s16(BMP180_CAL_MB)     # INT16
		self.cal_MC  = self._read_s16(BMP180_CAL_MC)     # INT16
		self.cal_MD  = self._read_s16(BMP180_CAL_MD)     # INT16

	def read_raw_temp(self):
		"""Reads the raw (uncompensated) temperature from the sensor."""
		self._write_byte(BMP180_CONTROL, BMP180_READTEMPCMD)
		time.sleep(0.005)  # Wait 5ms
		MSB = self._read_byte(BMP180_TEMPDATA)
		LSB = self._read_byte(BMP180_TEMPDATA+1)
		raw = (MSB << 8) + LSB
		return raw

	def read_raw_pressure(self):
		"""Reads the raw (uncompensated) pressure level from the sensor."""
		self._write_byte(BMP180_CONTROL, BMP180_READPRESSURECMD + (self._mode << 6))
		if self._mode == BMP180_ULTRALOWPOWER:
			time.sleep(0.005)
		elif self._mode == BMP180_HIGHRES:
			time.sleep(0.014)
		elif self._mode == BMP180_ULTRAHIGHRES:
			time.sleep(0.026)
		else:
			time.sleep(0.008)

		MSB = self._read_byte(BMP180_PRESSUREDATA)

	        LSB = self._read_byte(BMP180_PRESSUREDATA+1)

	        XLSB = self._read_byte(BMP180_PRESSUREDATA+2)

		raw = ((MSB << 16) + (LSB << 8) + XLSB) >> (8 - self._mode)
		print raw
		return raw

	 

	def read_temperature(self):
		"""Gets the compensated temperature in degrees celsius."""

		UT = self.read_raw_temp()

		X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15

		X2 = (self.cal_MC << 11) / (X1 + self.cal_MD)

		B5 = X1 + X2
		
		temp = ((B5 + 8) >> 4) / 10.0

		return temp

	def read_pressure(self):
	        """Gets the compensated pressure in Pascals."""

		UT = self.read_raw_temp()
	        UP = self.read_raw_pressure()

		X1 = ((UT - self.cal_AC6) * self.cal_AC5) >> 15

		X2 = (self.cal_MC << 11) / (X1 + self.cal_MD)

		B5 = X1 + X2

		# Pressure Calculations

		B6 = B5 - 4000

		X1 = (self.cal_B2 * (B6 * B6) >> 12) >> 11

		X2 = (self.cal_AC2 * B6) >> 11

		X3 = X1 + X2

		B3 = (((self.cal_AC1 * 4 + X3) << self._mode) + 2) / 4

		X1 = (self.cal_AC3 * B6) >> 13

		X2 = (self.cal_B1 * ((B6 * B6) >> 12)) >> 16

		X3 = ((X1 + X2) + 2) >> 2
		
		B4 = (self.cal_AC4 * (X3 + 32768)) >> 15
		
		B7 = (UP - B3) * (50000 >> self._mode)
		
		
		if B7 < 0x80000000:

			p = (B7 * 2) / B4
		
		else:
		
			p = (B7 / B4) * 2
		
			X1 = (p >> 8) * (p >> 8)
		
			X1 = (X1 * 3038) >> 16
		
			X2 = (-7357 * p) >> 16
		
			p = p + ((X1 + X2 + 3791) >> 4)
		
		return p
		
	 
		
	def read_altitude(self, sealevel_pa=101325.0):
		"""Calculates the altitude in meters."""
		# Calculation taken straight from section 3.6 of the datasheet.
		print self.read_pressure();
		pressure = float(self.read_pressure())
	
		altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0/5.255)))
		
		return altitude

	def read_sealevel_pressure(self, altitude_m=0.0):
		print self.read_pressure();
		pressure = float(self.read_pressure())
	
		p0 = pressure / pow(1.0 - altitude_m/44330.0, 5.255)
	
		return p0
