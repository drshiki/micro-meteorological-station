import DHT11.DHT11_driver as DHT11
import BH1750.BH1750_driver as BH1750
import BMP180.BMP180_driver as BMP180
import sys
import MySQLdb
import time

while True:
	item ={}
	tmp = DHT11.dht11_read()
	if  temp is not None
		item.update(tmp)
	else
		item.update({'humidity' : 0})
	item.update(BH1750.bh1750_read())
	item.update(BMP180.bmp180_read())

	print "humidity = %d %% RH" %(item['humidity'])
	print "illuminance = %.2f lx" %(item['illuminance'])
	print "temperature = %.1f *C" %(item['temperature'])
	print "pressure = %.1f hPa" %(item['pressure'])
	print "altitude = %.2f m" %(item['altitude'])

	conn = MySQLdb.Connection(host="localhost", user="root", passwd="123456",\
	charset="UTF8")
	conn.select_db('mms')
	cursor = conn.cursor()
	cursor.execute("insert into t_data(humidity, temperature, illuminance, ppm, \
	altitude, pressure, sea_level_press, time) values(%s, %s, %s, %s, %s, %s, %s, null)", \
	(item['humidity'], item['temperature'], item['illuminance'], 0, item['altitude'], \
	item['pressure'], 0))
	conn.commit();
	cursor.close()
	conn.close()
	time.sleep(1800)