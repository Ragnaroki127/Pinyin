from train_dataset import *
from viterbi import *
import os
import math
import sys

if __name__ == '__main__':
    hanzi_list = store_hanzi_list('../dataset/graph_data/pinyin_list.txt')
    hanzi_trans = pickle.load(open('../weights/hanzi_trans.pkl', 'rb'))
    hanzi_freq = pickle.load(open('../weights/hanzi_freq.pkl', 'rb'))
    fw = open('../data/output.txt', 'w')
    with open('../data/input.txt', encoding='utf-8') as fr:
        for line in fr.readlines():
            if line != '\n' and line[-1] == '\n':
                target = line[:-1].split(' ')
                optimized_phrase = viterbi_custom(hanzi_list, target, hanzi_trans, hanzi_freq)
                fw.write(optimized_phrase)
                fw.write('\n')
            elif line != '\n' and line[-1] != '\n':
                target = line.split(' ')
                optimized_phrase = viterbi_custom(hanzi_list, target, hanzi_trans, hanzi_freq)
                fw.write(optimized_phrase)
                fw.write('\n')
            else:
                continue