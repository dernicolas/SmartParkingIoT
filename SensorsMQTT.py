#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
import math
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import date, datetime

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins zuweisen
GPIO_TRIGGER_Sensor1 = 18
GPIO_ECHO_Sensor1 = 24

GPIO_TRIGGER_Sensor2 = 5
GPIO_ECHO_Sensor2 = 13

OLD_STATUS = 0
DISTANCE_THRESHOLD = 70

OLD_STATUS_Sensor2 = 0
DISTANCE_THRESHOLD_Sensor2 = 70

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_Sensor1, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Sensor1, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_Sensor2, GPIO.OUT)
GPIO.setup(GPIO_ECHO_Sensor2, GPIO.IN)

GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("arn:aws:iot:us-east-2:835754930850:thing/ParkingPi")
myMQTTClient.configureEndpoint("a11y1mnti3riv7.iot.us-east-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/cert/CA.pem", "/home/pi/cert/dc2175ba01-private.pem", "/home/pi/cert/dc2175ba01-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("thing01/info", "connected", 0)


def distanz1():
    #LEDs
    GPIO.output(26,GPIO.HIGH)
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER_Sensor1, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Sensor1, False)
 
    StartZeit1 = time.time()
    StopZeit1 = time.time()
 
    # speichere Startzeit
    while GPIO.input(GPIO_ECHO_Sensor1) == 0:
        StartZeit1 = time.time()
 
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO_Sensor1) == 1:
        StopZeit1 = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed1= StopZeit1 - StartZeit1
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz1 = (TimeElapsed1 * 34300) / 2
 
    return distanz1

def distanz2():
    #LEDs
    GPIO.output(26,GPIO.HIGH)
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER_Sensor2, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_Sensor2, False)
 
    StartZeit2 = time.time()
    StopZeit2 = time.time()
 
    # speichere Startzeit
    while GPIO.input(GPIO_ECHO_Sensor2) == 0:
        StartZeit2 = time.time()
 
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO_Sensor2) == 1:
        StopZeit2 = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed2= StopZeit2 - StartZeit2
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz2 = (TimeElapsed2 * 34300) / 2
 
    return distanz2


if __name__ == '__main__':
    try:
        while True:
            neueDistanz1=distanz1()
            if math.fabs((neueDistanz1-OLD_STATUS))>=DISTANCE_THRESHOLD:
                OLD_STATUS=neueDistanz1
                if neueDistanz1>=10:
                    iso_time = time.strftime("%Y-%m-%d-T%H:%M:%S")
                    print("Sensor 1 frei")
                    #GPIO.output(21,GPIO.LOW)
                    #GPIO.output(20,GPIO.HIGH)
                    x = 1
                    msg1 = '{"Sensor_ID": "Sensor1", "TimeStamp": '+ '"' + iso_time + '"' + ', "Status": "frei"}'
                    myMQTTClient.publish("pi01", msg1, 0)
                else:
                    iso_time = time.strftime("%Y-%m-%d-T%H:%M:%S")
                    print("Sensor1 belegt")
                    #GPIO.output(21,GPIO.HIGH)
                    #GPIO.output(20,GPIO.LOW)
                    x = 0
                    msg1 = '{"Sensor_ID": "Sensor1", "TimeStamp": '+ '"' + iso_time + '"' + ', "Status": "belegt"}'
                    myMQTTClient.publish("pi01", msg1, 0)
                
            neueDistanz2=distanz2()
            if math.fabs((neueDistanz2-OLD_STATUS_Sensor2))>=DISTANCE_THRESHOLD_Sensor2:
                OLD_STATUS_Sensor2=neueDistanz2
                if neueDistanz2>=10:
                    iso_time = time.strftime("%Y-%m-%d-T%H:%M:%S")
                    print("Sensor 2 frei")
                    #GPIO.output(21,GPIO.LOW)
                    #GPIO.output(20,GPIO.HIGH)
                    y = 1
                    msg2 = '{"Sensor_ID": "Sensor2", "TimeStamp": '+ '"' + iso_time + '"' + ', "Status": "frei"}'
                    myMQTTClient.publish("pi01", msg2, 0)
                else:
                    iso_time = time.strftime("%Y-%m-%d-T%H:%M:%S")
                    print("Sensor2 belegt")
                    #GPIO.output(21,GPIO.HIGH)
                    #GPIO.output(20,GPIO.LOW)
                    y = 0
                    msg1 = '{"Sensor_ID": "Sensor2", "TimeStamp": '+ '"' + iso_time + '"' + ', "Status": "belegt"}'
                    myMQTTClient.publish("pi01", msg1, 0)
                    
            if x == 0 and y == 0:               
                GPIO.output(21,GPIO.HIGH)
                GPIO.output(20,GPIO.LOW)
            else:
                GPIO.output(21,GPIO.LOW)
                GPIO.output(20,GPIO.HIGH)                
            time.sleep(1)

         
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()
