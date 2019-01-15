# mqtt References
import time
import paho.mqtt.client as mqtt
import time

# api references
import requests
import json

def on_message(client, userdata, message):
        #print("message topic=",message.topic + " - " + str(message.payload.decode("utf-8")))
        for L1 in Config['MQTT_Subscribe']:
                for L2 in L1['Rec']:
                        MQTT_Subscribe = L2['MQTT']
                        if message.topic == MQTT_Subscribe:
                                print("matched " + message.topic )
                                for L3 in L2['data']:
                                        CameraTag = L3['CameraTag']
                                        CameraID = L3['CameraID']
                                        CameraName = L3['CameraName']

                                        s = requests.Session()
                                        response = requests.get("http://xxx:7080/api/2.0/camera/")

                                        url = "http://xxx:7080/api/2.0/camera/" + CameraID + "?apiKey=xxx"
                                        MessageString = CameraTag + " (" + str(message.payload.decode("utf-8")) + "°c)"
                                        data = { "name": CameraName, "osdSettings": { "tag": MessageString } }
                                        headers = {"Content-Type" : "application/json"}

                                        response = requests.put(url, data=json.dumps(data), headers=headers )
                                        MessageSent = 'request: ' + str(response.status_code) + ', CameraID: ' + CameraID + ', Message:' + MessageString
                                        print(MessageSent)


while True:
        try:
                print("Starting")
                with open('/etc/UnifiCamera.json','r') as ConfigFile:
                        Config = json.load(ConfigFile)
                broker_address = "xx.xx.xx.xx"
                print("creating new instance")
                client = mqtt.Client("UnifiCamera") #create new instance
                client.on_message=on_message #attach function to callback
                print("connecting to broker")
                client.connect(broker_address) #connect to broker
                client.loop_start() #start the loop
                #SubString = "openhab/in/Bedroom2Heater/Temp"
                SubString = "openhab/in/#"
                print("Subscribing to topic",SubString)
                #client.subscribe("openhab/in/#")
                client.subscribe(SubString)
                time.sleep(3600) # wait
                client.loop_stop() #stop the loop
        except:
                time.sleep(10) # wait
