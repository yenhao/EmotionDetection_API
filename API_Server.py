# -*- coding:utf-8 -*-
from flask import Flask, json, request, Response
from flask_restful import reqparse, abort, Api, Resource
import classifier
import json
from pprint import pprint
import multiprocessing as mp
from time import gmtime, strftime
from OpenSSL import SSL

app = Flask(__name__)
api = Api(app)

pool = mp.Pool(processes=mp.cpu_count()-1)
print('[Classifier] {} - Using {} Core to process emotion classifier'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()) ,mp.cpu_count()-1))


'''
Handle Multi Message using Multi-process
'''
@app.route('/chuck/couple', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        # print(request.json)
        js = json.dumps(classifier.classifyUsingMatrixMulti(request.json, pool = pool))

        return Response(js, status=200, mimetype='application/json')
    else:
        return "415 Unsupported Data Type"

@app.route('/chuck/couple_all', methods = ['POST'])
def api_all():
    if request.headers['Content-Type'] == 'application/json':
        js = json.dumps(classifier.classifyUsingMatrixMulti(request.json, pool = pool, all_content = True))

        return Response(js, status=200, mimetype='application/json')
    else:
        return "415 Unsupported Data Type"

@app.route('/emomap/couple', methods = ['POST'])
def api_emo():
    if request.headers['Content-Type'] == 'application/json':
        js = json.dumps(classifier.classifyUsingMatrixMulti(request.json, pool = pool, all_content = True, story=True))

        return Response(js, status=200, mimetype='application/json')
    else:
        return "415 Unsupported Data Type"

@app.route('/chuck/test')
def test():
    data = {"data" : [{"message": "看不到你的號碼因為我們這樣分析的"},{"message": "好的那歡迎你直到了晚上去體驗看看"}]}
    return json.dumps(classifier.classifyUsingMatrixMulti(data))

if __name__ == '__main__':
    # app.run(debug=True)
    context = ('ssl.cert', 'ssl.key')
    app.run('0.0.0.0',debug = False, port=5678)
    # app.run(host='0.0.0.0',port='5678', 
    #     debug = False, ssl_context=context)