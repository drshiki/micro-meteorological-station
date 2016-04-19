# Author: touchEngine
#
# This file is part of micro-meteorological-station project.
# MQ135_driver.py - the core code to read temperature and pressure from BMP180.
#
# All softwares of this project can be modified, contributed, redistributed
# freely (without any limitation or payment), including all documents in this
# project. And this notice also is unnecessary to be included in your copy.

import time
import MCP3002.MCP3002_driver as mcp

def mq135_read():
	api = mcp.readAnalog(0, 0)
	return {'API':api}
