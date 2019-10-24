from train_dataset import *
from viterbi import *
import os
import math
import sys

if __name__ == '__main__':
    #程序输入格式：python3 main.py -i -o
    #argv[1]为输入的拼音文件，argv[2]为输出的汉字文件
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    #载入拼音汉字对照表
    hanzi_list = store_hanzi_list('../dataset/graph_data/pinyin_list.txt')
    #载入预训练模型，即转移频率和汉字出现频率
    hanzi_trans = pickle.load(open('../weights/hanzi_trans.pkl', 'rb'))
    hanzi_freq = pickle.load(open('../weights/hanzi_freq.pkl', 'rb'))
    #打开输出文件
    fw = open('../data/' + output_file, 'w')
    #打开输入文件
    with open('../data/' + input_file, encoding='utf-8') as fr:
        #读取每一行拼音
        for line in fr.readlines():
            #判断是否为空行
            if line != '\n' and line[-1] == '\n':
                #将字符串转化为数组，例'qing hua da xue\n'->['qing', 'hua', 'da', 'xue']
                target = line[:-1].split(' ')
                #调用viterbi算法，得到最佳匹配的汉字输出
                optimized_phrase = viterbi_custom(hanzi_list, target, hanzi_trans, hanzi_freq)
                #将结果输出到目标文件中
                fw.write(optimized_phrase)
                fw.write('\n')
            #文件最后一行结尾无换行，直接调用split方法得到数组即可
            elif line != '\n' and line[-1] != '\n':
                target = line.split(' ')
                optimized_phrase = viterbi_custom(hanzi_list, target, hanzi_trans, hanzi_freq)
                fw.write(optimized_phrase)
                fw.write('\n')
            else:
                continue
