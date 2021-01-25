import json
from pyhanlp import *
# 分词时只需要词，不需要词性
HanLP.Config.ShowTermNature = False

filepath = "peopledailyfianl.json"
a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

emotionDictionary={}
with open("dictionaryOfEmotion.json","r",encoding="utf-8") as f:
    emotionDictionary=json.load(f)

keyword=["自信","欣喜","惊讶","振奋","焦虑","恐惧","愤怒","悲伤"]
date=[]
result={}
for i in range(len(a)-1):
    if a[i+1]["发布时间"] not in date:
        date.append(a[i+1]["发布时间"])
for i in range(len(date)):
    result[date[i]]={}
    for key in keyword:
        result[date[i]][key]=0
is5=False
for i in range(len(a)-1):
    if a[i+1]["发布时间"]=="2019-12-20":
        break
    if a[i+1]["发布时间"]=="2020-06-20":
        is5=True
    if is5:
        print("在分析"+str(a[i+1]["发布时间"]))
        word=HanLP.segment(str(a[i+1]["微博内容"]+str(a[i+1]["评论"])))
        for item in word:
            for key in keyword:
                if str(item) in eval(emotionDictionary[key]):
                    result[a[i+1]["发布时间"]][key]=result[a[i+1]["发布时间"]][key]+1
        print(result)
        file = open("result.json", "w", encoding="utf-8")
        file.write(json.dumps(result, indent=4, ensure_ascii=False))
        file.close()

