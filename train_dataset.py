import os
import pickle

#判断一个字符是否是汉字，返回True或False
def isChinese(c):
    return u'\u4e00' <= c <= u'\u9fff'

#判断一个字符串中是否有汉字，返回True或False
def isChineseString(s):
    return any(u'\u4e00' <= c <= u'\u9fff' for c in s)

#模型训练函数，输入为语料库文件夹，文件默认编码方式为utf-8
def train(dir_name, encoding_method = 'utf-8'):
    #初始化字典，分别用于存放转移频率和出现频率
    hanzi_trans = {}
    hanzi_freq = {}
    #语料库文件序列
    file_list = os.listdir(dir_name)
    #遍历语料库文件
    for txt in file_list:
        with open(dir_name + txt, encoding = encoding_method) as f:
            for line in f.readlines():
                #判断行是否含有文字
                if len(line.strip()) < 2:
                    continue
                #若文字行格式非字符串则解码
                if not isinstance(line, str):
                    line = line.decode(encoding_method)
                #若该行无汉字则继续
                if not isChineseString(line.strip()):
                    continue
                #对该行进行处理，去掉收尾多余字节(line.strip())，再进行遍历，若为汉字则保留否则用空格代替
                #最后存储在数组中 eg. [' ', ' ', '原', '标', '题'，’ ‘，’新‘, '华'，‘社’，......]
                hanzi_list = [hanzi if isChinese(hanzi) else ' ' for hanzi in line.strip()]
                #以下代码作用是去除多余的空格，并得到原句中由标点隔开的短句
                #分别为标记短句开头的标志位、保存短句字符串的数组以及临时保存短句的字符串
                flag_head = True
                sub_sentences = []
                sub = ''
                #遍历hanzi_list
                for i in range(len(hanzi_list)):
                    #若为一个短句开头的空格（行开头空格或原先标点位置的空格），继续运行
                    if flag_head and hanzi_list[i] == ' ':
                        continue
                    #若开头标志位仍为1而遍历元素不为空格，则该元素为短句的第一个汉字，添加到sub中
                    #同时flag_head置位False
                    elif flag_head and hanzi_list[i] != ' ':
                        sub += hanzi_list[i]
                        flag_head = False
                    #短句中的汉字依次添加到sub中
                    elif not flag_head and hanzi_list[i] != ' ':
                        sub += hanzi_list[i]
                    #遍历至短句后的第一个空格则短句结束，将得到的短句sub添加到sub_sentences中
                    #sub清零，短句标志位置1，继续下一轮遍历
                    elif not flag_head and hanzi_list[i] == ' ':
                        if len(sub) > 0:
                            sub_sentences.append(sub)
                            sub = ''
                            flag_head = True
                #每行的最后一个短句之后可能无空格，故不会进入最后一个elif，此时将其添加至sub_sentences
                if len(sub) > 0:
                    sub_sentences.append(sub)
                #遍历每个短句
                for sub in sub_sentences:
                    #对每个短句中的汉字进行遍历
                    for i in range(len(sub)):
                        #如果该汉字未在hanzi_freq字典的键值中则将其添加到字典中并将其频率置1
                        #hanzi_freq的键值为对应的汉字，值为其出现频率
                        if sub[i] not in hanzi_freq.keys():
                            hanzi_freq[sub[i]] = 1
                        #若该汉字在hanzi_freq字典的键值中则将其频率加1
                        else:
                            hanzi_freq[sub[i]] += 1
                        #计算转移频率，转移频率与遍历到的汉字和它后一个汉字有关，因而
                        #每个短句的最后一个汉字不用计算转移频率
                        if i != len(sub) - 1:
                            #hanzi_trans的键值为当前汉字，其值亦为一个字典，该字典的键值为当前汉字的后
                            #一个汉字，其值为两者同时出现的频率
                            #如hanzi_trans = {'一':{'个': 1976, '群': 897, ...}, ...}
                            #以下计算每个短句中出现汉字的转移频率（除最后一个字）
                            if sub[i] not in hanzi_trans.keys():
                                hanzi_trans[sub[i]] = {}
                                hanzi_trans[sub[i]][sub[i + 1]] = 1
                            else:
                                if sub[i + 1] not in hanzi_trans[sub[i]].keys():
                                    hanzi_trans[sub[i]][sub[i + 1]] = 1
                                else:
                                    hanzi_trans[sub[i]][sub[i + 1]] += 1
    #返回转移频率和出现频率
    return hanzi_trans, hanzi_freq

#将得到的转移和出现频率字典存储至pickle文件中
#ht_file_name和hf_file_name分别是存储转移和出现频率的pickle文件名
def load_results_to_pickle(ht_file_name, hf_file_name, hanzi_trans, hanzi_freq):
    with open(ht_file_name, 'wb') as fout:
        pickle.dump(hanzi_trans, fout, True)

    with open(hf_file_name, 'wb') as fout:
        pickle.dump(hanzi_freq, fout, True)
    return

#计算单个汉字的出现概率
def score_single(ch, hanzi_trans, hanzi_freq):
    #如果该汉字在语料库中出现过，即在hanzi_freq的键值中
    if ch in hanzi_freq.keys():
        #语料库的总字数由hanzi_freq的所有值（每个汉字的出现频率）求和得到
        total = sum(hanzi_freq.values())
        #出现概率等于该汉字出现的频率除以总字数
        score = hanzi_freq[ch] / total
    #若未出现则概率为0
    else:
        score = 0
    return score

#计算两个汉字前后出现的转移概率，ch2为前面的字，ch1为出现在后面的字
def score_double(ch1, ch2, hanzi_trans, hanzi_freq):
    #转移概率为P(ch1|ch2) = P(ch2, ch1) / P(ch2)
    if ch2 in hanzi_trans.keys() and ch1 in hanzi_trans[ch2].keys():
        score = hanzi_trans[ch2][ch1] / hanzi_freq[ch2]
    else:
        score = 0
    return score

#运行主函数，将训练语料库得到的hanzi_trans和hanzi_freq存储到pickle文件中
if __name__ == '__main__':
    dir_name = '../dataset/train_data/'
    hanzi_trans, hanzi_freq = train(dir_name)
    load_results_to_pickle('../weights/hanzi_trans.pkl', '../weights/hanzi_freq.pkl', hanzi_trans, hanzi_freq)
    




