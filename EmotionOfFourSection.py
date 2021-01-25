import json
from pyhanlp import *
# 分词时只需要词，不需要词性
HanLP.Config.ShowTermNature = False

result={"19.12.8-2020.1.22":"","1.23-2.7":"","2.8-2.13":"","3.10-6.25":""}
keyword=["自信","欣喜","惊讶","振奋","焦虑","恐惧","愤怒","悲伤"]

emotionDictionary={}
with open("dictionaryOfEmotion.json","r",encoding="utf-8") as f:
    emotionDictionary=json.load(f)

for date in result:
    print(date)
    # if date=="19.12.8-2020.1.22":
    #     continue
    result[date]={}
    for key in keyword:
        result[date][key]=0
    file=open("highlight/"+str(date)+".json","r",encoding="utf-8")
    a=file.read()
    word = HanLP.segment(str(a))
    print("分词over")
    for item in word:
        for key in keyword:
            if str(item) in eval(emotionDictionary[key]):
                result[date][key] = result[date][key] + 1

    print(result)
    file = open("highlight/highlightResult.json", "w", encoding="utf-8")
    file.write(json.dumps(result, indent=4, ensure_ascii=False))
    file.close()

