import json
import os
from flask import Flask, Response, request
from flask_cors import CORS
from IRengine import *
from rankingEngine import *

app = Flask(__name__)
CORS(app)
dataProcessor = DataProcessor() 

@app.route('/getTitles', methods= ['GET'])
def getTitles():
    try:
        data = dataProcessor.titles_data
        data = data.to_json() 
        js = json.dumps(data)
        response = Response(js, status=200, mimetype='application/json')
        return response

    except Exception as e:
        print ("EROR", e)
        errMsg = "Something went wrong! ERROR: " + str(e) 
        js = json.dumps(errMsg)
        response = Response(js, status=400, mimetype='application/json')
        return response


@app.route('/applySearchModels', methods= ['GET', "POST"]) #needs to return relevant tweets and corresponding precision scores
def applySearchModels():
    try:
        jsonData = request.get_json()
        searchModel = jsonData["data"]
        articleTitle = jsonData["queryTitle"]
        articleId = jsonData["articleId"]
        pandas_df = dataProcessor.returnTweetsBasedOnSearchModel(articleId = articleId, articleTitle = articleTitle, searchModel = searchModel)
        return_data = {}
        return_data["pandas_data"] = pandas_df.to_json()
        return_data["ranking_score"] = [RANKING_MODEL, get_rank(pandas_df)]
        js = json.dumps(return_data)
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