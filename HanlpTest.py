# coding=utf-8
from pyhanlp import *
# HanLP.Config.ShowTermNature = False
import json

filepath = "peopledailyfianl.json"

a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

# print(HanLP.segment(a[2]))
word=HanLP.segment(str(a[1]["评论"]))
print(HanLP.segment(str(a[1]["评论"])))
for i in range(len(word)):
    word[i]=str(word[i].word)

# mouth = []
# for i in range(7):
#     mouth.append([])
#
# for i in range(len(a) - 1):
#     s = ""
#     s = a[i + 1]['发布时间']
#     mouth[int(s[5:7]) % 12].append(a[i + 1])
#
# for n in range(7):
#     file = open(str(n) + ".text", "w", encoding="utf-8")
#     text = ""
#     for i in range(len(mouth[n])):
#         text = text + mouth[n][i]['微博内容']
#         text = text + str(mouth[n][i]['评论'])
#         print("在写"+str(n)+"月的第"+str(i)+"篇")
#     print("在提取"+str(n)+"月的关键词")
#     TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
#     keyword_list = HanLP.extractKeyword(text, 1000)
#     file.write(",".join(keyword_list))
#     file.close()

# text=""
# for i in range(len(mouth_1)):
#     text=text+mouth_1[i]['微博内容']
#     text = text + str(mouth_1[i]['评论'])
#
# TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
# keyword_list = HanLP.extractKeyword(text, 1000)


# 每月关键词提取
# file2=open("2.text","w",encoding="utf-8")
# text2=""
# for i in range(len(mouth_2)):
#     text2=text+mouth_2[i]['微博内容']
#     text2 = text2 + str(mouth_2[i]['评论'])
# TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
# keyword_list = HanLP.extractKeyword(text2, 1000)
# file2.write(",".join(keyword_list))
# file2.close()


# 读取微博内容和评论
# for i in range(100):
#     print(a[i+1]['微博内容'])
#     print(a[i+1]['评论'])


# file=open(filepath,"r",encoding='utf-8')


# print(HanLP.segment(text))
# 提取关键词
# TextRankKeyword = JClass("com.hankcs.hanlp.summary.TextRankKeyword")
# keyword_list = HanLP.extractKeyword(text, 1000)

# i=0
# for item in keyword_list:
#     print(item+',',end="")
#     i=i+1
#     if i%20==0:
#         print("\n")
