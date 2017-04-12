# -*- coding:utf-8 -*-
import codecs
import unicodedata
import re
from os import listdir
from os.path import isfile, join, basename
import numpy as np
import multiprocessing as mp
import sys
from multiprocessing import Process
from Regemotest import pattern_match
from time import gmtime, strftime

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

def remove_control_characters(s):
    return u"".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def loadModels(path):
    print ("Loading Models")
    models = {}
    onlyFiles = [ f for f in listdir(path) if isfile(join(path,f)) ]   

    for f in onlyFiles:
        
        if "DS_Store" in f:
            continue
        print ("Processing "+f)
        emotion = f.split(".")[0]
        f = join(path,f)
        f = codecs.open(f,"r",encoding='utf-8') 

        patts = {}
               
        pos = 0 
        for line in f:
            
            #print line
            tokens = line.split("\t")
                        
            pattern = remove_control_characters(tokens[0].strip())
                     
            pos = pos + 1
            patts[pattern] =  pos

                     
        models[emotion] = patts

    return models;

def loadMatrix(path):
    #print "Loading matrix "+path

    f = codecs.open(path,"r",encoding='utf-8')

    emotions = {}
    patterns = {}

    matrix = []

    inEmotions = 0
    inPatterns = 0
    inMatrix = 0

    for line in f:
        line = line.strip()

        if "Emotions" in line:
            inEmotions = 1
            continue

        if "Patterns" in line:
            inPatterns = 1
            inEmotions = 0
            continue

        if "Matrix" in line:
            inMatrix = 1
            inPatterns = 0
            inEmotions = 0
            continue

        if inEmotions and len(line) > 0:
            #print "Emotion "+line
            tokens = line.split("\t");
            emotions[int(tokens[0])] = remove_control_characters(tokens[1].strip())
        
        if inPatterns and len(line) > 0:  
            tokens = line.strip().split("\t")
            patt = remove_control_characters(tokens[1].strip())
            patterns[int(tokens[0])] =  patt

            '''if len(patt) < 2:
                print "Small pattern "+patt'''
        
        if inMatrix and len(line) > 0: 
            row = [];
            tokens = line.split(" ");
            
            for val in tokens:
                row.append(float(val))
    
            matrix.append(row)
    
    return emotions, patterns, np.array(matrix)     

    

def evalWithMultiple(post, emotion,emotionModel):
    post = remove_control_characters(post)
    finalScore = 0.0
    for patt in emotionModel:
        #prog = re.compile(patt)
        #result = prog.finditer(post)
        #result = re.finditer(pattern, line, re.UNICODE)
        #for match in result:
            #print patt+" "+match.group(0)+" "+str(emotionModel[patt]  )  
        #    finalScore = finalScore + emotionModel[patt];
        sep_pattern = patt.split("<pw>")
        i = 0
        combine_word = u""
        while i < len(word_list):
            word = word_list[i]
            if word == " " or word == "　":
                word = u"_blank_"
            if sep_pattern[0] != "":
                if i == 0:
                    if word in sep_pattern[0]:
                        combine_word = word
                        if combine_word == sep_pattern[0]:
                            #i += (len(sep_pattern) - 1)
                            combine_word = u""
                            if (i + (len(sep_pattern) - 1)) < len(word_list):
                                count += 1
                    else:
                        combine_word = u""
                else:
                     if word in sep_pattern[0]:
                         combine_word = combine_word + word
                         if combine_word == sep_pattern[0]:
                             #i += (len(sep_pattern) - 1)
                             combine_word = u""
                             #print pattern + "\t" + str(i) + "\t" + str(len(word_list))
                             if (i + (len(sep_pattern) - 1)) < len(word_list):
                                 count += 1
                                 #print pattern
                     else:
                         combine_word = u""
            else:
                pos = len(sep_pattern)-1
                if i == 0:
                    if word in sep_pattern[pos]:
                        combine_word = word
                        if combine_word == sep_pattern[pos]:
                            if ((i - len(combine_word) + 1) - pos) >= 0:
                                count += 1
                            combine_word = u""
                    else:
                        combine_word = u""
                else:
                    if word in sep_pattern[pos]:
                        combine_word = combine_word + word
                        if combine_word == sep_pattern[pos]:
                            if ((i - len(combine_word) + 1) - pos) >= 0:
                                count += 1
                                #print pattern + "\t" + str(i) + "\t" + str(pos)
                            combine_word = u""
                    else:
                        combine_word = u""
            i += 1
        
    print (emotion+"\t"+str(finalScore))
    
    return finalScore  


def evalWithMatrix(post,emotions,patterns,matrix):
    print('[Classifier] {} - Processing : {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()) ,post))
    '''
    Start to handle emotion classifier
    '''
    post = remove_control_characters(post)
    word_list = pattern_match(post) 
    vector = []
    for index in patterns:
        #print index
        patt = patterns[index]
        count = 0;
        sep_pattern = patt.split("<pw>")
        i = 0
        combine_word = u""
        while i < len(word_list):
            word = word_list[i]
            if sep_pattern[0] != "":
                if i == 0:
                    if word in sep_pattern[0]:
                        combine_word = word
                        if combine_word == sep_pattern[0]:
                            combine_word = u""
                            if (i + (len(sep_pattern) - 1)) < len(word_list):
                                count += 1
                    else:
                        combine_word = u""
                else:
                     if word in sep_pattern[0]:
                         combine_word = combine_word + word
                         if combine_word == sep_pattern[0]:
                             combine_word = u""
                             if (i + (len(sep_pattern) - 1)) < len(word_list):
                                 count += 1
                     else:
                         combine_word = u""
            else:
                pos = len(sep_pattern)-1
                if i == 0:
                    if word in sep_pattern[pos]:
                        combine_word = word
                        if combine_word == sep_pattern[pos]:
                            if ((i - len(combine_word) + 1) - pos) >= 0:
                                count += 1
                            combine_word = u""
                    else:
                        combine_word = u""
                else:
                    if word in sep_pattern[pos]:
                        combine_word = combine_word + word
                        if combine_word == sep_pattern[pos]:
                            if ((i - len(combine_word) + 1) - pos) >= 0:
                                count += 1
                            combine_word = u""
                    else:
                        combine_word = u""
            i += 1   
        
        vector.append(count)
    vector = np.transpose(np.array(vector))
    #print vector
    result = np.dot(matrix,vector)
    order = np.argsort(result)

    result_dict = {}
    for i in order:
        emotion = emotions[i]
        score = result[i]
        result_dict[emotion] = score
        #print emotion + "\t" +str(score)

    emotion = emotions[order[0]]
    emotion2 = emotions[order[1]]
    
    #news:88880.0    joy:85079.0 anticipation:70876.0    fear:51043.0    anger:71064.0   surprise:78956.0    trust:76015.0   sadness:63041.0 disgust:61514.0
    if result_dict[emotion] == 0 and result_dict[emotion2] == 0:
        ambiguous = "True"
    else:
        ambiguous = "False"

    post_emotion = {
                "message": post,
                "emotion1": emotion,
                "emotion2": emotion2,
                "ambiguous": ambiguous
              }
    # print(post_emotion)
    return post_emotion



minFreq = 20
matrixPath = 'matrix_' + str(minFreq)
print('[Classifier] {} - Loading Matrix : {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()) ,matrixPath))


'''
Multi processing needed
'''
Matrix = loadMatrix(matrixPath)
print('[Classifier] {} - Using {} Core to process emotion classifier'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime()) ,mp.cpu_count()-1))


def classifyUsingMatrixMulti(data, Matrix = Matrix):
    '''
    Input: 
        posts [JSON]
        e.g.
        { data : [
          {
            "message": "抽顯卡做研究 DeepLearning + 黑色沙漠",
            ...
          },
          {
            "message": "送趙奕誠出國報conference",
            ...
          }...
          ]
        }
    Output:
        emotion_result [JSON]
        e.g.
        { data : [
          {
            "message": "抽顯卡做研究 DeepLearning + 黑色沙漠",
            "emotion1": "anger",
            "emotion2": "haha",
            "ambiguous" "True"
          },
          {
            "message": "送趙奕誠出國報conference",
            "emotion1": "Sad",
            "emotion2": "anger",
            "ambiguous" "False"
          }...
          ]
        }
    '''


    pool = mp.Pool(processes=mp.cpu_count()-1)

    [emotions,patterns,matrix] = Matrix
    emotion_result = {"data":[]}

    multi_res = [pool.apply_async(evalWithMatrix, (post.get('message'),emotions,patterns,matrix,)) for post in data.get('data') if post.get('message')] # for multi processing

    emotion_result['data'] = [res.get(timeout=1) for res in multi_res]

    return emotion_result



def classifyUsingMatrix(data, Matrix = Matrix):
    '''
    Input: 
        posts [JSON]
        e.g.
        { data : [
          {
            "message": "抽顯卡做研究 DeepLearning + 黑色沙漠",
            ...
          },
          {
            "message": "送趙奕誠出國報conference",
            ...
          }...
          ]
        }
    Output:
        emotion_result [JSON]
        e.g.
        { data : [
          {
            "message": "抽顯卡做研究 DeepLearning + 黑色沙漠",
            "emotion1": "anger",
            "emotion2": "haha",
            "ambiguous" "True"
          },
          {
            "message": "送趙奕誠出國報conference",
            "emotion1": "Sad",
            "emotion2": "anger",
            "ambiguous" "False"
          }...
          ]
        }
    '''
    [emotions,patterns,matrix] = Matrix
    emotion_result = {"data":[]}

    post = data.get('data')[0].get('message')
    if post:
        emotion_result['data'] = [evalWithMatrix(post,emotions,patterns,matrix)]
    else:    
        emotion_result['data'] = ['Empty Message']

    return emotion_result

