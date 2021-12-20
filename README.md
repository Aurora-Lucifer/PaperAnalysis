# PaperAnalysis
对于各类会议的accepted paper进行分析

## 项目介绍
* main.py 【带整合】
* utils.py 包含构建论文title库的必要函数
* analysis.py 包含现阶段已有的基于数据库实现的衍生功能

## 数据库基本格式
- xxx_year
  - xxx_title.txt
  - xxx-year.html
  - 其他衍生功能结果【待开发】

## 衍生功能
- 词频分析
  - 对某个会议进行title关键词分析（可过滤不必要词汇）
  - 输出文件title_analysis.json
- 查询功能
  - 根据给出的关键词提取论文题目
    【由于部分数学公式的存在，该查询不保证完整性】

## 开发计划
- 目前功能
    1. title提取
    2. 词频分析
    3. key words统计
- 考虑更多功能
    1. 爬虫模块
    2. 考虑查询功能
    3. 获得abstract
    4. 根据key words输出论文题目
    5. 相似功能关联
- 后面实时拉取各个官网内容
- 同步更多信息源
- 简单页面发【？？】