# coding=utf-8
from pyhanlp import *
import json

# 这部分代码是通过对每个月的新闻文本及其评论进行关键词提取，取每个月的前1000个关键词
filepath = "peopledailyfianl.json"

a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

# 从文件中读到七个月中
month = []
for i in range(7):
    month.append([])

for i in range(len(a) - 1):
    s = ""
    s = a[i + 1]['发布时间']
    month[int(s[5:7]) % 12].append(a[i + 1])

# 分别对不同的月份的新闻进行关键词提取
for n in range(7):
    file = open("keyword/"+str(n) + ".text", "w", encoding="utf-8")
    text = ""
    for i in range(len(month[n])):
        text = text + month[n][i]['微博内容']
        text = text + str(month[n][i]['评论'])
        print("在写"+str(n)+"月的第"+str(i)+"篇")
    print("在提取"+str(n)+"月的关键词")
    TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
    # 我们选择了提取每个月的前1000个关键词
    keyword_list = HanLP.extractKeyword(text, 1000)
    file.write(",".join(keyword_list))
    file.close()