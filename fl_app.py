from flask import Flask, url_for
from flask import request
import json, ast, re
from bson.json_util import dumps
import yaml
from influxdb import InfluxDBClient
import influx_db

app = Flask(__name__)

@app.route('/')
def api_root():
    print "inside the root"
    return 'Welcome'

@app.route('/alert', methods = ['GET', 'POST', 'PUT'])
def api_alert():
    if request.method == 'GET':
        return "ECHO: GET\n"
    elif request.method == 'POST':
        d = yaml.load(request.data)
        match_messages =  d.get("check_result").get("matching_messages")
        for match_message in match_messages:
            message_time =  match_message.get("timestamp")
            message_content =  match_message.get("message")
            msg_search = re.search(r'\[.*]', message_content).group()
            print msg_search.replace("[","").replace("]","")
            #print message_time
        source =  d.get("check_result").get("triggered_condition").get("title")
        message = d.get("check_result").get("result_description")
        print "Source %s and Message : %s" % (source, message)
        number_messages = re.findall(r'(Stream had \d+)', message)[0].split()[2]
        inser_alert(source, number_messages )
        return ""

def inser_alert(source, number_messages):
    pass
    client  = influx_db.influx_services()
    client.store_alert_callback(source, number_messages)



if __name__ == '__main__':
    app.run(host= '0.0.0.0')

