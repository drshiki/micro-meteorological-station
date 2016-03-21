import time
import MCP3002.MCP3002_driver as mcp

def yl83_read():
	rainfall = mcp.readAnalog(0, 1)
	return {'rainfall' : rainfall}
	
