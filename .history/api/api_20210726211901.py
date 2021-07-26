import json
import os
from flask import Flask, Response, request
from flask_cors import CORS
from IR_engine import DataProcessor


app = Flask(__name__)
CORS(app)
dataProcessor = DataProcessor()
# end-point to just check server status
@app.route('/',methods=["GET"])
def api_root():
    try:
        data = {
            'message': 'Server is up and running!'
        }
        js = json.dumps(data)
        response = Response(js, status=200, mimetype='application/json')
        return response
    except Exception as e:
        errMsg = "Something went wrong! ERROR: " + str(e) 
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        return response

# actual parsing method
@app.route('/api', methods= ['POST'])
def process_query():
    try:
        print(request)
        data = {
            'message': 'Successfully processed!',
        }
        js = json.dumps(data)
        # delete the stl file after done parsing
        response = Response(js, status=200, mimetype='application/json')
        return response

    except Exception as e:
        errMsg = "Something went wrong! ERROR: " + str(e) 
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        return response

@app.route('/getTitles', methods= ['GET'])
def getTitles():
    try:
        print(request)
        data = dataProcessor.data
        js = json.dumps(data)
        # delete the stl file after done parsing
        response = Response(js, status=200, mimetype='application/json')
        return response

    except Exception as e:
        print ("EROR", e)
        errMsg = "Something went wrong! ERROR: " + str(e) 
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)