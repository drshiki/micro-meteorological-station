# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# DHT11/test.py - the code test for reading temperature and humidity from DHT11.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import DHT11_driver;
data = DHT11_driver.dht11_read();
if data:
	print "temp = %d *C"%data['temperature'];
	print "humi = %d%% RH"%data['humidity'];
else:
	print "data is wrong, try again";

