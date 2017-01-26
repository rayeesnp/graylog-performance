import argparse

from influxdb import InfluxDBClient
import datetime
import time, math

class influx_services:

    def __init__(self):
        self.host = 'localhost'
        self.port = 8086
        dbname  = 'graylog'
        self.influx = InfluxDBClient( self.host, self.port, 'root', 'root')
        self.influx.switch_database(dbname)
        #self.influx.write_points()


    def store_alert_callback(self, source, number_messages):

        now = datetime.datetime.today()
        points = []
        measurement = "alert_out"
        number_messages = int(number_messages)
        alert_out = {
            "measurement": measurement,
        #    "time": int(now.strftime('%s')),
            "fields": {
            "process": source,
            "messages": number_messages
            }
        }
        points.append(alert_out)
        self.influx.write_points(points)

    def view_alert(self):
        query = 'SELECT * FROM foobar'
        print("Queying data: " + query)
        result = self.influx.query(query, database='graylog')
        print("Result: {0}".format(result))

# if __name__ == '__main__':
#     store_alert_callback()
