import mms.DHT11.DHT11_driver as DHT11
import mms.BH1750.BH1750_driver as BH1750
import mms.BMP180.BMP180_driver as BMP180
import sys;
import MySQLdb;

data1 = DHT11.dht11_read();
data2 = BH1750.bh1750_read();
data3 = BMP180.bmp180_read();

print "humidity = %d %% RH" %data1[0];
print "illuminance = %.2f lx" %data2;
print "temperature = %.1f * C" %data3[0];
print "pressure = %.1f Pa" %data3[1];
print "altitude = %.2f m" %data3[2]; 

conn = MySQLdb.Connection(host="localhost", user="root", passwd="123456", charset="UTF8")
conn.select_db('mms')

cursor = conn.cursor()
#cursor.execute("insert into t_data(humidity) values(1)")
cursor.execute("insert into t_data(humidity,temperature,illuminance,ppm,altitude,pressure,ser_level_press,time) values(%s,%s,%s,%s,%s,%s,%s, null)" ,(data1[0],data3[0],data2,0,data3[2],data3[1],0))
conn.commit();
cursor.close()

conn.close()
