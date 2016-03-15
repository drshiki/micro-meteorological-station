import DHT11_driver;
data = DHT11_driver.dht11_read();
if data != False:
	print "temp = %d *C"%data[1];
	print "humi = %d%% RH"%data[0];
else:
	print "data is wrong, try again";

