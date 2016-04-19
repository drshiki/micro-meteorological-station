# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# MQ135/test.py - the code test for reading temperature and humidity from DHT11.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import sys
sys.path.append('..')
import MQ135_driver

data = MQ135_driver.mq135_read()
print "API = %d"%data['API']

