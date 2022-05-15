from distutils.log import error
import uuid
import random

import numpy as np

from datetime import datetime

import paho.mqtt.client as mqtt

class Device:
    """
    This is the main class to simulate a sensor device.
    """
    def __init__(self, measure, min_val, max_val, mean_val=0, std_val=1, given_uuid=None, battery=True, decading_factor=0.000001, malfunctioning_rate=0.02):
        self.uuid = str(uuid.uuid4()) if given_uuid is None else given_uuid
        self.measure = measure 
        self.mean_val = mean_val
        self.std_val = std_val
        self.min_val = min_val
        self.max_val = max_val
        self.decading_factor = decading_factor
        self.malfunctioning_rate = malfunctioning_rate
        self.recordings_queue = []
        self.recorded_measures = 0
        self.n_outliers = 0
        self.n_errors = 0

    def __repr__(self):
        return f"Device UUID {self.uuid} to record measure: {self.measure}"
    
    def simulate_recording(self):
        rec = {}
        rec["uuid"] = self.uuid
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
        
        self.recordings_queue.append(rec)

    