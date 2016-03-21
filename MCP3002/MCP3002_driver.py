# (c) BotBook.com - Karvinen, Karvinen, Valtokari

# Installing spidev:
# sudo apt-get update
# sudo apt-get -y install git python-dev
# git clone https://github.com/doceme/py-spidev.git
# cd py-spidev/
# sudo python setup.py install

import spidev # installation help in botbook_mcp3002.py comments
import time

def readAnalog(device = 0,channel = 0):
	assert device in (1, 0)
	assert channel in (1, 0)
	#open spi
	spi = spidev.SpiDev()
	spi.open(0, device)
	"""
	Protocol start bit (S), sql/diff (D), odd/sign (C), MSBF (M)
	Use leading zero for more stable clock cycle
	0000 000S DCM0 0000 0000 0000
	Sending 3 8bit packages so xpi.xfer2 will return the same amount.
	start bit = 1
	sql/diff = 1 SINGLE ENDED MODE (2 channel mode)
	odd/sign = channel 0/1
	MSBF = 0
	"""
	command = [1, (2 + channel) << 6, 0]
	#2 + channel shifted 6 to left
	#10 or 11 << 6 = 1000 0000 or 1100 0000
	reply = spi.xfer2(command)
	"""
	Parse right bits from 24 bit package (3*8bit)
	We need only data from last 2 bytes.
	And there we can discard last two bits to get 10 bit value
	as MCP3002 resolution is 10bits
	Discard reply[0] byte and start from reply[1] where our data starts
	"""
	value = reply[1] & 31
	#31 = 0001 1111 with & operation makes sure that we have all data from XXXX DDDD and nothing more. 0001 is for signed in next operation.
	value = value << 6 #Move to left to make room for next piece of data.
	#000D DDDD << 6 = 0DDD DD00 0000
	#Now we get the last of data from reply[2]
	value = value + (reply[2] >> 2)
	#Here we discard last to bits
	#DDDD DDXXX >> 2 = 00DD DDDD
	#0DDD DD00 0000 + 00DD DDDD = 0DDD DDDD DDDD
	spi.close()
	return value
