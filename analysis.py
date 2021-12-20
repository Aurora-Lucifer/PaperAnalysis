# zym 2021.11.23
'''
    扩展功能:
        词频分析
        论文查询
'''

import re
import os
import json
from utils import database_generate, read_all, save_all, path_generate

'''
data_path -> accept paper list 所在的html页面【暂无爬虫手动复制】
title_save_path -> title存储路径
analysis_path -> 词频分析结果存储路径
key -> html中
'''

conference_name = 'nips'
year_number = '2020'

# title_save_path = 'dataset/icml_2021/icml_title.txt'
# analysis_result = 'dataset/icml_2021/title_analysis.json'

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
    "Curriculum",
    # "active",
    # "active learning",
    # "selection",
    # "acquisition"
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


def count_analysis(conference, year, word_lenth):
    '''
    词频分析
        word_length表示要分析的词长度上限
    '''
    folder_name, _, title_save_path = path_generate(conference, year)
    titles = read_all(title_save_path)
    count = {}
    for i in range(word_lenth):
        count.update(words_frequency_analysis(titles, k=i+1))
    remove_useless_words(count)
    for words in key_words:
        if words in count.keys():
            print(words, count[words])
    count = sort_dict(count, 500)
    analysis_result = folder_name + '/title_analysis.json'
    json.dump(count, open(analysis_result, 'w'), indent=-1)


def title_selection(key_words: list, title_list: list):
    '''
        筛选title_list中含key_words的项
        输入两个list
        返回一个dict，key_words为键，对应选中的title列表为值
    '''
    ret = {}
    for key in key_words:
        ret[key] = []
        for title in title_list:
            if key in title:
                ret[key].append(title)
    return ret


def database_selection(conference_list=None, year_range=None):
    '''
        根据会议范围和年份范围选择需要的会议
            缺损状态默认全选
        返回一个 dict 键为"会议-年份"，值为title路径
    '''
    ret = {}
    database_list = os.listdir('dataset')
    for folder in database_list:
        if '_' in folder and '.' not in folder:
            conference, year = folder.split('_')
            # 判断会议和年份是否正确
            # 如果为None, 默认正确
            if (
                conference_list is None or conference in conference_list
            ) and (
                year_range is None or year in year_range
            ):
                target_path = 'dataset/' + folder
                file_list = os.listdir(target_path)
                for file_name in file_list:
                    if 'title.txt' in file_name:
                        target_path += '/' + file_name
                        ret[conference+'-'+year] = target_path
    return ret


def query_for_keywords(key_words, conference_list=None, year_range=None):
    title_paths = database_selection(conference_list, year_range)
    ret = {}
    # 查询
    for words in key_words:
        ret[words] = {}
    for target in title_paths.keys():
        titles = read_all(title_paths[target])
        query_ans = title_selection(key_words, titles)
        for words in key_words:
            ret[words][target] = query_ans[words]

    # 输出
    for words in key_words:
        print(words)
        for target in ret[words].keys():
            if len(ret[words][target]) != 0:
                print(target)
                for title in ret[words][target]:
                    print(title, end='')

    return ret


if __name__ == "__main__":
    # count_analysis(conference_name, year_number, 3)
    ans = query_for_keywords(key_words)
