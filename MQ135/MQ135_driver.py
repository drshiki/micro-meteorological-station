import time
import MCP3002.MCP3002_driver as mcp

def mq135_read():
	api = mcp.readAnalog(0, 0)
	return {'API':api}
