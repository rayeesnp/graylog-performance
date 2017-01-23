from flask import Flask, url_for
from flask import request
import json, ast
from bson.json_util import dumps
import yaml

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
        source =  d.get("check_result").get("triggered_condition").get("title")
        message = d.get("check_result").get("result_description")
        print "Source %s and Message : %s" % (source, message)
        return ""

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
