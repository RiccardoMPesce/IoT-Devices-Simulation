import json
import uuid
import random
import time

import numpy as np

from datetime import datetime

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Received from topic " + msg.topic + " message: " + str(msg.payload))

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Granted QoS {granted_qos}")

class Device:
    """
    This is the main class to simulate a sensor device.
    """
    def __init__(self, measure, min_val, max_val, mean_val=0, std_val=1, given_uuid=None, decading_factor=0.000001, malfunctioning_rate=0.02, queue_max_size=10000):
        self.id = str(uuid.uuid4()) if given_uuid is None else given_uuid
        self.measure = measure 
        self.mean_val = mean_val
        self.std_val = std_val
        self.min_val = min_val
        self.max_val = max_val
        self.decading_factor = decading_factor
        self.malfunctioning_rate = malfunctioning_rate
        self.queue_max_size = queue_max_size
        self.recordings_queue = []
        self.recorded_measures = 0
        self.n_outliers = 0
        self.n_errors = 0

    def establish_connection(self, broker_url, broker_port, clean_session=0, keep_alive=60):
        self.client = mqtt.Client(clean_session=0, client_id=self.id)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect(broker_url, broker_port, keep_alive)
        self.client.loop_start()

    def __repr__(self):
        return f"Device {self.id} to record measure: {self.measure}"
    
    def simulate_recording(self):
        rec = {}
        rec["id"] = self.id
        rec["measure"] = self.measure
        
        malfunctioning = bool(np.random.binomial(1, self.malfunctioning_rate, 1)[0])
        
        if malfunctioning:
            rec["value"] = float("nan")
            rec["health"] = "error"
            self.n_errors += 1
        else:
            rec["value"] = rec["value"] = round(random.uniform(self.min_val, self.max_val) + (random.gauss(self.mean_val, self.std_val)), 2)
            rec["health"] = "ok"
        
        rec["timestamp"] = str(datetime.utcnow())
        self.recorded_measures += 1

        if rec["value"] < self.min_val or rec["value"] > self.max_val:
            self.n_outliers += 1
        
        if len(self.recordings_queue) > self.queue_max_size:
            self.recordings_queue = []
        
        self.recordings_queue.append(rec)
        
        return rec

    def publish_recordings(self, n=1, sleep_s=1.0, topic="riccardo/pesce/test", retain=0, qos=0):
        for i in range(n):
            self.client.publish(topic, json.dumps(self.simulate_recording()), retain=retain, qos=qos)
            time.sleep(sleep_s)

    def subscribe(self, *topics_with_qos):
        self.client.subscribe(topics_with_qos)