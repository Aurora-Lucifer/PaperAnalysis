# zym 2021.11.23
'''
    词频分析
    对于所有的2021的ICML accept paper的title进行词频的分析
    输入https://icml.cc/Conferences/2021/Schedule?type=Poster的html文件
    输出title的词频分析
    目前功能
        1. title提取
        2. 词频分析
        3. key words统计
    考虑更多功能
        1. 爬虫模块
        2. 考虑查询功能
        3. 获得abstract
        4. 根据key words输出论文题目
        5. 相似功能关联
'''
import re
import json

'''
data_path -> accept paper list 所在的html页面【暂无爬虫手动复制】
title_save_path -> title存储路径
analysis_path -> 词频分析结果存储路径
key -> html中
'''

# data_path = 'dataset/icml_2021/ICML-2021.html'
# title_save_path = 'dataset/icml_2021/icml_title.txt'
# analysis_result = 'dataset/icml_2021/title_analysis.json'
# key = 'maincardBody'

# data_path = 'dataset/nips_2021/NIPS-2021.html'
# title_save_path = 'dataset/nips_2021/nips_title.txt'
# analysis_result = 'dataset/nips_2021/title_analysis.json'
# key = 'maincardBody'

data_path = 'dataset/kdd_2021/KDD-2021.html'
title_save_path = 'dataset/kdd_2021/kdd_title.txt'
analysis_result = 'dataset/kdd_2021/title_analysis.json'
key = 'font color'


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
    # "deep", "neural", "network",
    # "learning", "networks",
    # "learning for", "for deep"
]


key_words = [
    # 搜索目标key word
    "detection"
    "anomaly",
    "outlier",
    "novelty",
    "out-of-distribution",
    "one-class",
    "fraud",
    "robust",
    "noise",
    "anomaly detection",
    "outlier detection",
    "novelty detection",
    "out-of-distribution detection",
    "one-class detection",
    "fraud detection",
    "anomalous"
]


def title_extract(data, title_key):
    '''
    抽取题目，删除无关项
    输入
        data是一个html根据\n切分出的list
        title_key是html中标志title的提示属性
    返回所有论文title
    '''
    title_list = []
    for line in data:
        if title_key in line:
            n = 1
            while n > 0:
                line, n = re.subn(r"\<[^<]*?\>", "", line)
            # import ipdb; ipdb.set_trace()
            title = line.strip() + '\n'
            title_list.append(title)
    return title_list


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


def remove_useless_words(count_dict:dict):
    for words in UseLessWords:
        if words in count_dict:
            count_dict.pop(words)
    return count_dict


def sort_dict(count_dict, threshold=None):
    temp = sorted(
        count_dict.items(), key=lambda x:x[1], reverse=True
    )
    if threshold is not None:
        temp = temp[:threshold]
    count_result = {}
    for item in temp:
        count_result[item[0]] = item[1]
    return count_result


def read_all(file_path):
    f = open(file_path, 'r')
    data = f.readlines()
    f.close()
    return data


def save_all(data, file_path):
    f = open(file_path, 'w')
    f.writelines(data)
    f.close()


if __name__ == "__main__":
    data = read_all(data_path)
    titles = title_extract(data, title_key=key)
    save_all(titles, title_save_path)
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
