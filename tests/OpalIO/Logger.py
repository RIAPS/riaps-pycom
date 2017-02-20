from riaps.run.comp import Component
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
import json
import logging
from datetime import datetime
import os

DB_HOST = 'localhost'
DB_PORT = '8086'
DB_NAME = 'opalio'
DB_USER = 'riapsdev'
DB_PASSWORD = 'riaps'

class Logger(Component):
    def __init__(self):
        super().__init__()
        self.pid = os.getpid()
        self.logger.info("%s - starting",str(self.pid))
        self.client = InfluxDBClient(host=DB_HOST, port=DB_PORT,
            database=DB_NAME, username=DB_USER, password=DB_PASSWORD)

    def on_rx_c37data(self):
        raw, data = self.rx_c37data.recv_pyobj()
        # self.logger.info("on_rx_c37data()[%s]: %s", str(self.pid), repr(data))
        timestamp = int(1e9 * data['timestamp'])
        # alternative:
        # timestamp = datetime.utcfromtimestamp(data['timestamp'])
        point_values = [
            {
                "time": timestamp,
                "measurement": "pmu",
                "fields":  {
                    "VAGA": data["VAGA"],
                    "VASA": data["VASA"],
                },
                "tags": {
                    "Actor" : "OpalIOActor"
                },
            }
        ]
        self.client.write_points(point_values)
		# we add the code to add the data to

