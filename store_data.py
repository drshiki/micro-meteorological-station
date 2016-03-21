import DHT11.DHT11_driver as DHT11
import BH1750.BH1750_driver as BH1750
import BMP180.BMP180_driver as BMP180
import MQ135.MQ135_driver as MQ135
import YL83.YL83_driver as YL83
import sys
import MySQLdb
import time

while True:
	item ={}
	tmp = DHT11.dht11_read()
	if  tmp is not None:
		item.update(tmp)
	else:
		item.update({'humidity' : 0})
	item.update(BH1750.bh1750_read())
	item.update(BMP180.bmp180_read())
	item.update(MQ135.mq135_read())
	item.update(YL83.yl83_read())
	print "humidity = %d %% RH" %(item['humidity'])
	print "illuminance = %.2f lx" %(item['illuminance'])
	print "temperature = %.1f *C" %(item['temperature'])
	print "pressure = %.1f hPa" %(item['pressure'])
	print "altitude = %.2f m" %(item['altitude'])
	print "API = %.2f" %(item['API'])
	print "rainfall = %.1f" %(item['rainfall'])
	conn = MySQLdb.Connection(host="localhost", user="root", passwd="123456",\
	charset="UTF8")
	conn.select_db('mms')
	conn.autocommit(True);
	cursor = conn.cursor()
	cursor.execute("insert into t_data(humidity, temperature, illuminance, api, \
	altitude, pressure, sea_level_press, time, rainfall) values(%s, %s, %s, %s, %s, %s, %s, null, %s)", \
	(item['humidity'], item['temperature'], item['illuminance'], item['API'], item['altitude'], \
	item['pressure'], 0, item['rainfall']))
	#conn.commit();
	cursor.close()
	conn.close()
	time.sleep(1800)
