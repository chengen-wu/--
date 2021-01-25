import json

# 这里读取的是关键词合集，从而建立出情绪词典
filepath = "keyword.json"
a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

# 我们总共设定了八种情绪
keyword=["自信","欣喜","惊讶","振奋","焦虑","恐惧","愤怒","悲伤"]
word=[]
result={}
file=open("dictionaryOfEmotion.json","w",encoding="utf-8")
# 对每个情绪中的词汇进行去重工作
for key in keyword:
    word=str(a[key]).split(" ")
    result[key]=[]
    for item in word:
        if item in result[key]:
            pass
        else:
            result[key].append(item)
    result[key]=str(result[key])
# 保存情绪词典
file.write(json.dumps(result,indent=4,ensure_ascii=False))
file.close()