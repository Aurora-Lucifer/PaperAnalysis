# zym 2021.11.23
'''
    基础功能模块 -> 建立论文title查询库
    包含以下功能
    1. 爬虫获取页面
    2. html -> title
    3. 存储所有的title.txt
'''
import os
import re
import requests
'''
data_path -> accept paper list 所在的html页面
title_save_path -> title存储路径
key -> html中标志title的属性名称
'''

# data_path = 'dataset/icml_2021/ICML-2021.html'
# title_save_path = 'dataset/icml_2021/icml_title.txt'
# analysis_result = 'dataset/icml_2021/title_analysis.json'
# key = 'maincardBody'

url = 'https://nips.cc/Conferences/2020/Schedule?type=Poster'
conference_name = 'nips'
year_number = '2020'
key = 'maincardBody'
# data_path = 'dataset/nips_2021/NIPS-2021.html'
# title_save_path = 'dataset/nips_2021/nips_title.txt'
# analysis_result = 'dataset/nips_2021/title_analysis.json'

# data_path = 'dataset/kdd_2021/KDD-2021.html'
# title_save_path = 'dataset/kdd_2021/kdd_title.txt'
# analysis_result = 'dataset/kdd_2021/title_analysis.json'
# key = 'font color'


def path_generate(conference, year):
    '''
        生成各种需要的数据路径
    '''
    folder_name = 'dataset/' + conference + '_' + year
    data_path = folder_name + '/' + conference + '-' + year + '.html'
    title_path = folder_name + '/' + conference + '_title.txt'
    return folder_name, data_path, title_path


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


def get_html(url):
    html = requests.get(url)
    if html.status_code != 200:
        print("页面爬取错误")
    return html.text


def database_generate(url, conference, year, key):
    '''
        生成会议论文database
    '''
    # 获取页面
    html = get_html(url)
    # 路径生成
    folder_name, data_path, title_path = path_generate(conference, year)
    if os.path.exists(folder_name) is False:
        os.mkdir(folder_name)
    # 储存
    save_all(html, data_path)
    # TODO: Unicode -> utf-8，暂时懒得写转换了直接存了再读
    data = read_all(data_path)
    titles = title_extract(data, title_key=key)
    save_all(titles, title_path)


if __name__ == "__main__":
    database_generate(url, conference_name, year_number, key)
    # data = read_all(data_path)
    # titles = title_extract(data, title_key=key)
    # save_all(titles, title_save_path)
