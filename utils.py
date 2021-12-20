# zym 2021.11.23
'''
    基础功能模块 -> 建立论文title查询库
    包含以下功能
    1. 爬虫获取页面
    2. html -> title
    3. 存储所有的title.txt
'''
import re
import json

'''
data_path -> accept paper list 所在的html页面
title_save_path -> title存储路径
key -> html中标志title的属性名称
'''

data_path = 'dataset/icml_2021/ICML-2021.html'
title_save_path = 'dataset/icml_2021/icml_title.txt'
analysis_result = 'dataset/icml_2021/title_analysis.json'
key = 'maincardBody'

# data_path = 'dataset/nips_2021/NIPS-2021.html'
# title_save_path = 'dataset/nips_2021/nips_title.txt'
# analysis_result = 'dataset/nips_2021/title_analysis.json'
# key = 'maincardBody'

# data_path = 'dataset/kdd_2021/KDD-2021.html'
# title_save_path = 'dataset/kdd_2021/kdd_title.txt'
# analysis_result = 'dataset/kdd_2021/title_analysis.json'
# key = 'font color'


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
