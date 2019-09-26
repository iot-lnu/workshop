import time
import ubinascii
from machine import Pin
import utime
import pycom
import machine
from network import LoRa
import socket
import binascii
import ustruct

# initialise Ultrasonic Sensor pins
echo = Pin('P21', mode=Pin.IN) # Lopy4 specific: Pin('P20', mode=Pin.IN)
trigger = Pin('P23', mode=Pin.OUT) # Lopy4 specific Pin('P21', mode=Pin.IN)
trigger(0)

# Ultrasonic distance measurment
def distance_measure():
    # trigger pulse LOW for 2us (just in case)
    trigger(0)
    utime.sleep_us(2)
    # trigger HIGH for a 10us pulse
    trigger(1)
    utime.sleep_us(10)
    trigger(0)

    # wait for the rising edge of the echo then start timer
    while echo() == 0:
        pass
    start = utime.ticks_us()

    # wait for end of echo pulse then stop timer
    while echo() == 1:
        pass
    finish = utime.ticks_us()

    # pause for 20ms to prevent overlapping echos
    utime.sleep_ms(20)

    # calculate distance by using time difference between start and stop
    # speed of sound 340m/s or .034cm/us. Time * .034cm/us = Distance sound travelled there and back
    # divide by two for distance to object detected.
    distance = ((utime.ticks_diff(start, finish)) * .034)/2

    return distance

    # to reduce errors we take ten readings and use the median
def distance_median():

    # initialise the list
    distance_samples = []
    # take 10 samples and append them into the list
    for count in range(10):
        distance_samples.append(int(distance_measure()))
    # sort the list
    distance_samples = sorted(distance_samples)
    # take the center list row value (median average)
    distance_median = distance_samples[int(len(distance_samples)/2)]
    # apply the function to scale to volts

    print(distance_samples)

    return int(distance_median)


# disable LED heartbeat (so we can control the LED)
pycom.heartbeat(False)
# set LED to red
pycom.rgbled(0x7f0000)

# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("DevEUI: " + ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

# access info
app_eui = binascii.unhexlify('70B3D57ED00222DB')
app_key = binascii.unhexlify('095D815ABAD620C5F56896C0FCA865C4')

# attempt join - continues attempts background
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait for a connection
print('Waiting for LoRaWAN network connection...')
while not lora.has_joined():
	utime.sleep(1)
	# if no connection in a few seconds, then reboot
	if utime.time() > 15:
		print("possible timeout")
		machine.reset()
	pass

# we're online, set LED to green and notify via print
pycom.rgbled(0x004600)
print('Network joined!')

# setup the socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)
s.bind(1)

count = 0
# limit to 200 packets; just in case power is left on
while count < 200:

	# take distance measurment, turn the light blue when measuring
	pycom.rgbled(0x00007d)
	utime.sleep(1)
	distance = distance_median()
	pycom.rgbled(0x004600)

	print("Distance:  ", distance)
	# encode the packet, so that it's in BYTES (TTN friendly)
	# could be extended like this struct.pack('f', distance) + struct.pack('c',"example text")
    # 'h' packs it into a short, 'f' packs it into a float, must be decoded in TTN
	packet = ustruct.pack('h', distance)

	# send the prepared packet via LoRa
	s.send(packet)

	# example of unpacking a payload - unpack returns a sequence of
	#immutable objects (a list) and in this case the first object is the only object
	print ("Unpacked value is:", ustruct.unpack('h',packet)[0])

	# check for a downlink payload, up to 64 bytes
	rx_pkt = s.recv(64)

	# check if a downlink was received
	if len(rx_pkt) > 0:
		print("Downlink data on port 200:", rx_pkt)
		pycom.rgbled(0xffa500)
		input("Downlink recieved, press Enter to continue")
		pycom.rgbled(0x004600)

	count += 1
	utime.sleep(2)
