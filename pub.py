import paho.mqtt.client as mqtt
import time

client = mqtt.Client("adafdadff-112d12-112ddd")

client.connect("localhost", port=1883, keepalive=120)
client.subscribe("test/mosquitto/")

client.loop_start()

client.publish("test/mosquitto/", b"Ciao")

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

client.on_message = on_message

time.sleep(5)

client.loop_stop()