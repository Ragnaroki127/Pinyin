# 拼音输入法 V1.0
## I. 文件结构
1. data文件夹存放程序的输入输出文件，默认的是input.txt和output.txt。
2. dataset文件夹存放训练模型所需要的语料库和拼音汉字对照表，这两者分别存放在train_data和graph_data文件夹里。为了程序处理方便语料库文件皆被转为utf-8格式。
3. src文件夹存放程序源代码
* `main.py`是实现程序运行的主文件
* `train_dataset.py`实现模型的训练并输出训练结果
* `viterbi.py`实现viterbi算法并输出匹配程度最好的汉语结果
* `test.py`为临时测试文件，不参与程序运行
4. weights文件夹存放保存的训练结果，以加速程序运行

## II. 程序运行
1. 软件依赖：
* Python 3.7开发环境
* Pickle
2. 运行方式
    在Mac OS或Linux操作系统的bash终端运行：
* `python3 train_dataset.py`训练数据集，训练得到的输出储存在weights文件夹中
* `python3 main.py -i -o`运行程序，`-i`参数为输入文件，`-o`参数为输出文件。示例`python3 main.py input.txt output.txt`