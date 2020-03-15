# -*- coding: utf-8 -*-
import argparse  
import base64 
import httplib2 
import json
import math
import os
import select
import serial
import subprocess
import time
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from socket import socket, AF_INET, SOCK_DGRAM

GPIO.setup("P9_14", GPIO.OUT)
GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_36", GPIO.OUT)
GPIO.setup("P8_46", GPIO.OUT)

speech_file = '/root/test2.wav'
encoding = 'LINEAR16'
sampleRate = 16000
languageCode = 'zh-tw'

UART.setup("UART1")
ADC.setup()
DISCOVERY_URL = ('https://{api}.googleapis.com/$discovery/rest?'  
				 'version={apiVersion}')

def record_voice():
	subprocess.call('arecord -D plughw:1,0 -V mono -r 16000 -f S16_LE -d 3 /root/test2.wav', shell=True)
	
def get_speech_service():
	credentials = GoogleCredentials.get_application_default().create_scoped(
		['https://www.googleapis.com/auth/cloud-platform'])
	http = httplib2.Http()
	credentials.authorize(http)

	return discovery.build(
		'speech', 'v1beta1', http=http, discoveryServiceUrl=DISCOVERY_URL)

def main(speech_file):
	global Word
	with open(speech_file, 'rb') as speech:
		speech_content = base64.b64encode(speech.read())

	service = get_speech_service()
	service_request = service.speech().syncrecognize(
		body={
			'config': {
				'encoding': encoding,
				'sampleRate': sampleRate,  
				'languageCode': languageCode,  
			},
			'audio': {
				'content': speech_content.decode('UTF-8')
				}
			})
	response = service_request.execute()
	try:
		#取dist字串
		ss = response['results']
		s1 = ss[0]
		s2 = s1['alternatives']
		s3 = s2[0]
		Word = s3['transcript']
	except:
		#沒有語音輸入
		print("No Word Input!")

if __name__ == '__main__':
	print("wait for command ... ...")
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('', 11111))
	blink1 = 0; blink2 = 0; blink3 = 0; blink4 = 0
	redLED = "P8_36"; greenLED = "P9_14"; yellowLED = "P8_10"
	UART.setup("UART1")
	ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600)
	Wopen = u"開"; Wclose = u"關"; Wred = u"紅"; Wgreen = u"綠"; Wyellow = u"黃"
	Wall  = u"全部"; Wblink = u"閃爍"; Wsame = u"同時"; Wturn = u"輪流";
	Wtemp = u"溫度"; Wvoice = u"辨識"; Walways = u"恆"; Wtime = u"時間"
	
	Word = ''
	while True:
		data = 0; Word=''; rec = False; web = False;#初始化所有值
		ADC1value = ADC.read_raw("P9_40")
		ser.close()
		ser.open()
		if ADC1value == 4095: #偵測按鈕後錄音並解析
			rec = True
			ser.write("2")#顯示"REC"
			record_voice()
			ser.write("3")
			print
			main(speech_file)#進入辨識api
		
		s.setblocking(0)
		ready = select.select([s], [], [], 0.2) #設定websocket延時，0.2秒接收指令
		if ready[0]: #如果websocket接收到指令
			web = True
			data, addr = s.recvfrom(1024)
			print "Received %r from %s " % (data, addr)
		
		if rec == True or web == True: #如果有接收到socket或voice指令
			if rec == True and Wopen not in Word and Wclose not in Word and Wblink not in Word and Wtemp not in Word and Wvoice not in Word and Walways not in Word and Wtime not in Word:
				print u"沒有這個指令 %s" % Word
				ser.write("1 No such command")

			if data == "1" or (Wred in Word and Wopen in Word) or (Wred in Word and Walways in Word):
				GPIO.output("P8_36", GPIO.HIGH) #紅燈開
				blink1 = 0; redLED = "P8_46"
			elif data == "2" or (Wgreen in Word and Wopen in Word) or (Wgreen in Word and Walways in Word):
				GPIO.output("P9_14", GPIO.HIGH) #綠燈開
				blink2 = 0; greenLED = "P8_46"
			elif data == "3" or (Wyellow in Word and Wopen in Word) or (Wyellow in Word and Walways in Word):
				GPIO.output("P8_10", GPIO.HIGH) #黃燈開
				blink3 = 0; yellowLED = "P8_46"
			elif data == "4" or (Wred in Word and Wblink in Word):#紅燈閃爍
				blink1 = 1
			elif data == "5" or (Wgreen in Word and Wblink in Word):#綠燈閃爍
				blink2 = 1
			elif data == "6" or (Wyellow in Word and Wblink in Word):#黃燈閃爍
				blink3 = 1
			elif data == "7" or (Wred in Word and Wclose in Word):#紅燈關
				GPIO.output("P8_36", GPIO.LOW); blink1 = 0; redLED = "P8_46"
			elif data == "8" or (Wgreen in Word and Wclose in Word):#綠燈關
				GPIO.output("P9_14", GPIO.LOW); blink2 = 0; greenLED = "P8_46"
			elif data == "9" or (Wyellow in Word and Wclose in Word):#黃燈關
				GPIO.output("P8_10", GPIO.LOW); blink3 = 0; yellowLED = "P8_46"
			elif data == "10" or (Wall in Word and Wopen in Word) or (Wsame in Word and Wopen in Word):#全部開啟
				GPIO.output("P8_10", GPIO.HIGH); GPIO.output("P9_14", GPIO.HIGH); GPIO.output("P8_36", GPIO.HIGH)
				blink1 = 0; blink2 = 0; blink3 = 0; blink4 = 0
			elif data == "11" or (Wall in Word and Wclose in Word):#全部關閉
				GPIO.output("P8_10", GPIO.LOW);  GPIO.output("P9_14", GPIO.LOW);  GPIO.output("P8_36", GPIO.LOW)
				blink1 = 0; blink2 = 0; blink3 = 0; blink4 = 0
			elif data == "12" or (Wturn in Word and Wblink in Word):#輪流閃爍
				blink1 = 1; blink2 = 1; blink3 = 1
			elif data == "13" or (Wsame in Word and Wblink in Word):#同時閃爍
				blink4 = 1; blink1 = 0; blink2 = 0; blink3 = 0
				redLED = "P8_36"; greenLED = "P9_14"; yellowLED = "P8_10"
			elif data == "14" or (Wtemp in Word):#顯示溫度
				ser.write("0")
				ser.close()
			elif data == "15" or Wvoice in Word:#語音辨識
				ser.write("2")#顯示"REC"
				record_voice()
				ser.write("3")
				main(speech_file)
				ww = "1 " + Word
				try:
					ser.write(ww.encode())
				except:
					ser.write("1 Cannot Display Chinese")
				ser.close()
			elif data == "16" or Wtime in Word:#時間
				a = str(int(time.strftime("%H")) + 8)
				b = time.strftime("%Y/%m/%d ")
				c = time.strftime(":%M:%S")
				d = b + a + c
				ser.write("1 "+ d )
			time.sleep(.5)
			
		if blink1 == 1:
			GPIO.output("P8_36", GPIO.HIGH)
			time.sleep(.2)
			GPIO.output("P8_36", GPIO.LOW)
		if blink2 == 1:
			GPIO.output("P9_14", GPIO.HIGH)
			time.sleep(.2)
			GPIO.output("P9_14", GPIO.LOW)
		if blink3 == 1:
			GPIO.output("P8_10", GPIO.HIGH)
			time.sleep(.2)
			GPIO.output("P8_10", GPIO.LOW)
		if blink4 == 1:
			GPIO.output(redLED, GPIO.HIGH)
			GPIO.output(greenLED, GPIO.HIGH)
			GPIO.output(yellowLED, GPIO.HIGH)
			time.sleep(.2)
			GPIO.output(redLED, GPIO.LOW)
			GPIO.output(greenLED, GPIO.LOW)
			GPIO.output(yellowLED, GPIO.LOW)
			