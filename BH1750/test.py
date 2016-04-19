# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# BH1750/test.py - the code test for reading illuminance from BH1750.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import BH1750_driver

data = BH1750_driver.bh1750_read()
print "illuminance = %.2f lx" %data['illuminance']
