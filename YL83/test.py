# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# YL83/test.py - the code test for reading temperature and humidity from DHT11.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import sys
sys.path.append('..')
import YL83_driver

data = YL83_driver.yl83_read()
print "rainfall = %d"%data['rainfall']

