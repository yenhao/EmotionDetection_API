# -*- coding:utf-8 -*-
from flask import Flask, json, request, Response
from flask_restful import reqparse, abort, Api, Resource
import classifier
import json
from pprint import pprint
import multiprocessing as mp

app = Flask(__name__)
api = Api(app)


# data = json.loads(open('input.json').read(), encoding="UTF-8")

# pool = mp.Pool(processes=mp.cpu_count()-1)

 # classifier.classifyUsingMatrix(data)

 # classifier.classifyUsingMatrixMulti(data)

# api.add_resource(ChuckClassifier, '/chuck/single')

# api.add_resource(ChuckClassifierMulti, '/chuck/couple')

'''
Handle Multi Message using Multi-process
'''
@app.route('/chuck/couple', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        # print(request.json)
        js = json.dumps(classifier.classifyUsingMatrixMulti(request.json))

        return Response(js, status=200, mimetype='application/json')
    else:
        return "415 Unsupported Data Type"

@app.route('/chuck/test')
def test():
    return json.dumps(classifier.classifyUsingMatrixMulti(data))

if __name__ == '__main__':
    # app.run(debug=True)
    app.run('0.0.0.0',debug = False, port=5678)