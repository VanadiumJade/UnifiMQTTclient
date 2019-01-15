# mqtt References
import time
import paho.mqtt.client as mqtt

# api references
import requests
import json

#defaults
FailureRestart = "10"

def on_message(client, userdata, message):
	for L1 in Config['MQTT_Subscribe']:
		for L2 in L1['Rec']:
			MQTT_Subscribe = L2['MQTT']
			if message.topic == MQTT_Subscribe:
				print("matched " + message.topic )
				for L3 in L2['data']:
					CameraTag = L3['CameraTag']
					CameraID = L3['CameraID']
					CameraName = L3['CameraName']
					CameraTagPrefix = L3['CameraTagPrefix']
					CameraTagPostfix = L3['CameraTagPostfix']
					
					s = requests.Session()
					url = "http://" + Host + "/api/2.0/camera/" + CameraID + "?apiKey=" + API_Key
					MessageString = CameraTag + CameraTagPrefix + str(message.payload.decode("utf-8")) + CameraTagPostfix
					data = { "name": CameraName, "osdSettings": { "tag": MessageString } }
					headers = {"Content-Type" : "application/json"}
					
					response = requests.put(url, data=json.dumps(data), headers=headers )
					MessageSent = 'request: ' + str(response.status_code) + ', CameraID: ' + CameraID + ', Message:' + MessageString
					print(MessageSent)

while True:
	try:
		print("........................")
		print("Starting")
		with open('UnifiCamera.json','r') as ConfigFile:
			Config = json.load(ConfigFile)

		ConfigMain = Config['Config']
		print("........................")
		API_Key = ConfigMain[0]["API_Key"]
		Host = ConfigMain[0]["Host"]
		FailureRestart = ConfigMain[0]["FailureRestart"]
		MQTT_ForceReconnect = ConfigMain[0]["MQTT_ForceReconnect"]

		#Broker Config
		MQTT_Broker 		= ConfigMain[0]["MQTT_Broker"]
		MQTT_Name 			= ConfigMain[0]["MQTT_Name"]
		MQTT_Subscription 	= ConfigMain[0]["MQTT_Subscription"]

		print("FailureRestart: " + FailureRestart)
		print("MQTT_ForceReconnect: " + MQTT_ForceReconnect)
		print("MQTT_Broker: " + MQTT_Broker)
		print("MQTT_Name: " + MQTT_Name)
		print("MQTT_Subscription: " + MQTT_Subscription)
		print("API_Key: " + API_Key)
		print("........................")

		print("creating new instance")
		client = mqtt.Client(MQTT_Name) #create new instance
		client.on_message=on_message #attach function to callback
		print("connecting to broker " + MQTT_Broker + " with subscription=" + MQTT_Subscription)
		client.connect(MQTT_Broker) #connect to broker
		client.loop_start() #start the loop
		print("Subscribing to topic",MQTT_Subscription)
		client.subscribe(MQTT_Subscription)
		time.sleep(int(MQTT_ForceReconnect)) # wait
		client.loop_stop() #stop the loop
	except:
		time.sleep(FailureRestart) # wait