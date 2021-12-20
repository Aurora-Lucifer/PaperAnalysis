# zym 2021.11.23
'''
    扩展功能:
        词频分析
        论文查询
'''

import re
import json
from utils import read_all, save_all

'''
data_path -> accept paper list 所在的html页面【暂无爬虫手动复制】
title_save_path -> title存储路径
analysis_path -> 词频分析结果存储路径
key -> html中
'''

title_save_path = 'dataset/icml_2021/icml_title.txt'
analysis_result = 'dataset/icml_2021/title_analysis.json'

# title_save_path = 'dataset/nips_2021/nips_title.txt'
# analysis_result = 'dataset/nips_2021/title_analysis.json'

# title_save_path = 'dataset/kdd_2021/kdd_title.txt'
# analysis_result = 'dataset/kdd_2021/title_analysis.json'


# remove相关单词 remove_useless_words
UseLessWords = [
    "for", "with", "of",
    "and", "in", "a", "the",
    "via", "on", "to", "from",
    "using", "by", "an", "as",
    "over", "without", "is", "are",
    "towards", "under",
    "on the", "in the", "for the",
    "with a",
    # 辅助内容
    "deep", "neural", "network",
    "learning", "networks",
    "learning for", "for deep"
]


key_words = [
    "active",
    "active learning",
    "selection",
    "acquisition"
]


def words_frequency_analysis(data, k=1):
    '''
    函数对于整个输入数据进行词频分析
    输入
        data -> 文本
        k -> n个词的词频
    输出 词频分析结果【有序】
    '''
    count_dict = {}
    for line in data:
        text = line.lower().split()
        for i in range(k, len(text)):
            word_list = text[i-k:i]
            word = ' '.join(word_list)
            if word in count_dict.keys():
                count_dict[word] += 1
            else:
                count_dict[word] = 1
    return count_dict


def remove_useless_words(count_dict: dict):
    for words in UseLessWords:
        if words in count_dict:
            count_dict.pop(words)
    return count_dict


def sort_dict(count_dict, threshold=None):
    temp = sorted(
        count_dict.items(), key=lambda x: x[1], reverse=True
    )
    if threshold is not None:
        temp = temp[:threshold]
    count_result = {}
    for item in temp:
        count_result[item[0]] = item[1]
    return count_result


if __name__ == "__main__":
    titles = read_all(title_save_path)
    count = words_frequency_analysis(titles, k=1)
    count.update(words_frequency_analysis(titles, k=2))
    count.update(words_frequency_analysis(titles, k=3))
    remove_useless_words(count)
    for words in key_words:
        if words in count.keys():
            print(words, count[words])
    count = sort_dict(count, 500)
    json.dump(count, open(analysis_result, 'w'), indent=-1)

    # import ipdb; ipdb.set_trace()
