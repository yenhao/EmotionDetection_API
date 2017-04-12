# -*- coding:utf-8 -*-
import requests
import json
import urllib2


class EmotionDetection(object):
    """docstring for EmotionDetection"""
    def __init__(self):
        super(EmotionDetection, self).__init__()

    __url = 'http://192.168.2.23:5678/chuck/couple'

    def get_obj(self, texts_list):
        '''
        Input : [TEXT_LIST]
        Output: [JSON]
        '''
        # Prepare the query information
        query = {"data":[]}
        for text in texts_list:
            query["data"].append({"message":text})

        req = urllib2.Request(self.__url)
        req.add_header('Content-Type', 'application/json')

        # Send request
        response = urllib2.urlopen(req, json.dumps(query))

        return json.loads(response.read())



if __name__ == '__main__':
    em = EmotionDetection()

    texts_list = ['好無聊喔！','卡提諾狂新聞666']

    json = em.get_obj(texts_list)

    print(json['data'])