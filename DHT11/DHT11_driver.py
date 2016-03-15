import RPi.GPIO as GPIO;
import time;

debug = 1;
use_port = 12;
bit_count = 40;

def dht11_read():

	data = [];
	i = 0;
	
	GPIO.setmode(GPIO.BOARD);
	time.sleep(1); # DHT11 need 1 second to reach stable state after power-on
	GPIO.setup(use_port, GPIO.OUT);

	# the host sends a low level the begin signal to DHT11 lasting for 0.018 seconds at least
	GPIO.output(use_port, GPIO.LOW);
	time.sleep(0.02);

	# send a high level to tell DHT11 the begin signal is over
	GPIO.output(use_port, GPIO.HIGH);

	# begin to read signal from DHT11
	GPIO.setup(use_port, GPIO.IN);
	# whether the DHT11 havs sent the ack signal
	if GPIO.input(use_port) == GPIO.LOW:

		# this loop reads the ack signal from DHT11
		while GPIO.input(use_port) == GPIO.LOW:
			continue;

		# this loop insures the DHT11 ends the ack signal		
		while GPIO.input(use_port) == GPIO.HIGH:
			continue;

		while i < bit_count:
			k=0;
			# past the begin part of the first bit (the level in the 0.000012 ~ 0.000014 seconds)
			while GPIO.input(use_port) == GPIO.LOW:
				continue;
			# count the time of duration of the high level
			while GPIO.input(use_port) == GPIO.HIGH:
				if k>100:
					break;
				k+=1;
	
			if k<10: # warming! adjust this figure can affect error rate of reading
				data.append(0);
			else:
				data.append(1);
			i+=1;
		# get the temperature and humidity in decimalism
		humi = get_dec(data[0:8]);
		temp = get_dec(data[16:24]);
		check = get_dec(data[32:40]);
		
		if debug == 1:
			print "the humi = %d"%humi;
			print "the temp = %d"%temp;
			print "the check = %d"%check;	
				
		GPIO.cleanup();
		
		if humi + temp == check:
			return [humi,temp];
		else:
			return False;			
	else:
		if debug == 1:
			print "it is wrong, can not recieve the ack from DHT11, please check the use_port and hardware then try again"
		
		GPIO.cleanup();
		return False;

def get_dec(data):
	rs = 0;
	for i in range(8):
		rs += data[i] * 2 ** (7-i);
	return rs;	
