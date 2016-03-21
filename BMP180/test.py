# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# BMP180/test.py - the code to test for reading temperature and pressure
# from BMP180.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import BMP180_driver

data = BMP180_driver.bmp180_read()

print 'temperature = %.1f * C' %data[0]
print 'pressure = %.1f Pa' %data[1]
print 'altitude = %.2f m' %data[2]
print 'sea level pressure  = %.1f Pa' %data[3]
