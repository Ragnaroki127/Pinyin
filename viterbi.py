import os
import math
from train_dataset import *

#将拼音汉字对照表存储到字典中，该字典的键值为拼音，值为拼音对应的汉字
#例: hanzi_list = {'a': ['啊', '阿', '锕', ... ], ...}
def store_hanzi_list(hanzi_list_file):
    hanzi_list = {}
    with open(hanzi_list_file, encoding = 'gbk') as f:
        for line in f.readlines():
            if line[-1] == '\n':
                #若该行以换行符结尾则去掉换行符
                #例: line = 'an 安 按 案 ... 暗\n'
                line = line[:-1]
                content = line.split(' ')
                #键为每行第一个元素，即拼音
                key = content[0]
                #初始化键值对应的列表
                hanzi_list[key] = []
                #删除每行的第一个元素，即拼音
                del content[0]
                hanzi_list[key] = content
            else:
                content = line.split(' ')
                key = content[0]
                hanzi_list[key] = []
                del content[0]
                hanzi_list[key] = content
    return hanzi_list
#viterbi算法实现函数，https://blog.ailemon.me/2017/04/27/statistical-language-model-chinese-pinyin-to-words/
def viterbi_custom(hanzi_list, target, hanzi_trans, hanzi_freq):
    #设置每一步的概率阈值，剔除概率过低的句子
    prob_thresh = 0.001
    #py2han列表为实现算法的主要数据结构，其每一个值对应一个拼音
    #例：target = ['qing', 'hua', 'da', 'xue']
    py2han = []
    for i in range(len(target)):
        #初始化py2han列表
        #py2han = [{}, {}, {}, {}]
        py2han.append({})
    for i in range(len(target)):
        if i == 0:
            #例：ch == '清'
            for ch in hanzi_list[target[i]]:
                #得到‘清’的出现概率，即P('清')，设定第一步的阈值为1e-5
                if score_single(ch, hanzi_trans, hanzi_freq) > 1e-5:
                    #例：py2han = [{‘清’: score}, {}, {}, {}] 
                    py2han[i][ch] = score_single(ch, hanzi_trans, hanzi_freq)
        #例： ch == '华'
        else:
            #例：i == 1， pre == '清'， ch == '华'
            for pre in py2han[i - 1].keys():
                for ch in hanzi_list[target[i]]:
                    #例：P('清')*P('华'|'清') > 0.0001^2，设定第i步的阈值为0.001的i+1次方
                    #当i >= 2时pre字符串的长度大于1，因而取pre的最后一个字，即pre[i - 1]计算转移概率
                    if py2han[i - 1][pre] * score_double(ch, pre[i - 1], hanzi_trans, hanzi_freq) > math.pow(prob_thresh, i + 1):
                        #例：py2han = [{'清': score, '青': score, ...}, {'清华': score}, {}, {}]
                        py2han[i][pre + ch] = py2han[i - 1][pre] * score_double(ch, pre[i - 1], hanzi_trans, hanzi_freq)
    #取最后一步结束后得到的py2han的所有候选句                  
    candidate_phrases = py2han[len(target) - 1].keys() 
    #若最后一步结束后py2han列表的最后一个字典有内容
    if len(candidate_phrases) > 0: 
        #概率最高（score最大）的句子即为输出                   
        optimized_phrase = max(py2han[len(target) - 1], key = py2han[len(target) - 1].get)
    else:
        optimized_phrase = 'Sorry, we are not able to translate the sentence'
    return optimized_phrase
