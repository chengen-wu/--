import json
from pyhanlp import *
# 分词时只需要词，不需要词性
HanLP.Config.ShowTermNature = False

# 在这个文件中，我们统计出了八种不同的情绪在每天的新闻及其评论中出现的词频
filepath = "peopledailyfianl.json"
a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

emotionDictionary={}
with open("dictionaryOfEmotion.json","r",encoding="utf-8") as f:
    emotionDictionary=json.load(f)
# 初始化工作
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
isIn=False
# 这里开始统计词频
for i in range(len(a)-1):
    if a[i+1]["发布时间"]=="2019-12-20":
        break
    if a[i+1]["发布时间"]=="2020-06-20":
        isIn=True
    if isIn:
        print("在分析"+str(a[i+1]["发布时间"]))
        # 基本思想是将每天的每篇新闻内容及其评论进行分词，在这里我们采取了Hanlp库中的segmen()方法进行分词，然后对每个词汇进行匹配，如果这个词在我们的情绪词典中，那我们就将这一天的该种情绪频数+1
        word=HanLP.segment(str(a[i+1]["微博内容"]+str(a[i+1]["评论"])))
        for item in word:
            for key in keyword:
                if str(item) in eval(emotionDictionary[key]):
                    result[a[i+1]["发布时间"]][key]=result[a[i+1]["发布时间"]][key]+1
        print(result)
        # 在分析完每一篇以后进行结果的保存，防止中途出现问题而导致已处理的数据丢失
        file = open("result.json", "w", encoding="utf-8")
        file.write(json.dumps(result, indent=4, ensure_ascii=False))
        file.close()

