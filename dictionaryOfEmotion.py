import json

filepath = "keyword.json"
a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

keyword=["自信","欣喜","惊讶","振奋","焦虑","恐惧","愤怒","悲伤"]
word=[]
result={}
file=open("dictionaryOfEmotion.json","w",encoding="utf-8")
for key in keyword:
    word=str(a[key]).split(" ")
    result[key]=[]
    for item in word:
        if item in result[key]:
            pass
        else:
            result[key].append(item)
    result[key]=str(result[key])
file.write(json.dumps(result,indent=4,ensure_ascii=False))
file.close()