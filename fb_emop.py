# -*- coding:utf-8 -*-
import os
import json
import codecs
import urllib2
from pprint import pprint
from datetime import datetime

class EmotionDetection(object):
    """docstring for EmotionDetection"""
    def __init__(self):
        super(EmotionDetection, self).__init__()

    # __url = 'http://140.114.77.18:5678/emomap/couple'
    __url = 'http://140.114.77.18:5678/chuck/couple_all'

    def get_obj_from_text(self, texts_list):
        '''
        Input : [TEXT_LIST]
        Output: [JSON]
        '''
        # Prepare the query information
        query = {"data":[]}
        for text in texts_list:
            query["data"].append({"message":text, "datetime": datetime.now().strftime("%Y/%m/%d %H:%M:%S"), "story":"Huang Yen Hao at 清華名人堂."})

        req = urllib2.Request(self.__url)
        req.add_header('Content-Type', 'application/json')

        # Send request
        response = urllib2.urlopen(req, json.dumps(query))

        return json.loads(response.read())

    def get_obj_from_json(self, out_json):
        '''
        Input : [JSON]
        Output: [JSON]
        '''
        
        req = urllib2.Request(self.__url)
        req.add_header('Content-Type', 'application/json')

        # Send request
        response = urllib2.urlopen(req, json.dumps(out_json))

        return json.loads(response.read().encode('utf-8'))


def query(d, folder, filename):
    result_json = {}
    for key, val in d.iteritems():
        length = len(val)
        if length > 0 :
            batch = 16
            total_round = length / batch
            print('Total-Round : ' + str(total_round))
            result = []
            for i in xrange(total_round):
                out_json = {"data":val[ batch * i : batch * (i+1)]}
                # for dict_ in em.get_obj_from_json(out_json)['data']:
                    # dict_["message"] = dict_["message"].encode('utf-8')
                    # print(type(dict_["message"]))
                    # result.append(dict_)
                result += em.get_obj_from_json(out_json)['data']
                
            result_json[key] = result
        else:
            result_json[key] = []

    with codecs.open( folder + 'emo_' + filename, 'w', encoding='utf-8') as outfile:
        # outfile.write(json.dumps(result_json, ident=4), ensure_ascii=False)
        json.dump(result_json, outfile, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    '''
    create emotion detect object
    '''
    em = EmotionDetection()


    '''
    read json
    '''
    folder = 'fb/'
    file_lists = os.listdir(folder)

    for filename in os.listdir(folder):
        with open(folder+filename) as json_data:
            d = json.load(json_data)
            query(d, folder, filename)

