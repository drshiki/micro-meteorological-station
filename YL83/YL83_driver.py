# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# YL83_driver.py - the core code to read temperature and pressure from BMP180.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import time
import MCP3002.MCP3002_driver as mcp

def yl83_read():
	rainfall = mcp.readAnalog(0, 1)
	return {'rainfall' : rainfall}
	
