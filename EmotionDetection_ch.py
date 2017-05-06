# -*- coding:utf-8 -*-
import json
import urllib2
from datetime import datetime

class EmotionDetection(object):
    """docstring for EmotionDetection"""
    def __init__(self):
        super(EmotionDetection, self).__init__()

    # __url = 'http://0.0.0.0:5678/chuck/couple'

    __url = 'http://140.114.77.18:5678/emomap/couple'

    def get_obj(self, texts_list):
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



if __name__ == '__main__':
    em = EmotionDetection()

    texts_list = ['Apple不能作業系統阿Apple是IOS系統','看不到你的號碼因為我們這樣分析的','好的那歡迎你直到了晚上去體驗看看','4分鐘不只阿他他他覺得這樣速度很慢']

    json = em.get_obj(texts_list)

    print(json['data'])

    for js_obj in json['data']:
        output_format = '{}\nFirst Emotion : {}\nSecond Emotion : {}\nIs it Ambiguous : {}\n\n'.format(
                (js_obj.get('message')).encode('utf-8'), js_obj.get('emotion1'), js_obj.get('emotion2'), js_obj.get('ambiguous')
            )
        print(output_format)