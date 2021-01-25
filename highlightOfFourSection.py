import json

# 在这个文件中，我们取出来了四个不同阶段的重点新闻
filepath = "peopledailyfianl.json"
a = []
with open(filepath, "r", encoding='utf-8') as f:
    a = json.load(f)

# 我们对重点新闻的基本定义是：关注度远远高于其他新闻可被划分为重点新闻，因此我们采取了一篇新闻的 点赞数+评论数+转发数 作为比较的权重
for i in range(len(a) - 1):
    a[i+1]["权重"]=a[i+1]["转发数"]+a[i+1]["评论数"]+a[i+1]["点赞数"]

# 初始化
section = []
for i in range(4):
    section.append([])

# 我们先对四个阶段的新闻分好类
i=1
while True:
    if i==len(a):
        break
    s = a[i]['发布时间']
    if s=="2020-06-15":
        while True:
            if s=="2020-03-09":
                break
            section[3].append(a[i])
            i=i+1
            s=a[i]['发布时间']

    if s=="2020-02-13":
        while True:
            if s=="2020-02-08":
                break
            section[2].append(a[i])
            i=i+1
            s=a[i]['发布时间']

    if s=="2020-02-07":
        while True:
            if s=="2020-01-23":
                break
            section[1].append(a[i])
            i=i+1
            s=a[i]['发布时间']

    if s=="2020-01-22":
        while True:
            if s=="2019-12-08":
                break
            section[0].append(a[i])
            i=i+1
            s=a[i]['发布时间']
    i=i+1



# bubble sort
for n in range(4):
    for i in range(len(section[n])):
        for j in range(len(section[n])-1):
            if section[n][j]["权重"]<section[n][j+1]["权重"]:
                temp=section[n][j]
                section[n][j]=section[n][j+1]
                section[n][j+1]=temp

# 我们在写文件时，只取了该阶段内权重在前10%的新闻，这一类新闻被我们划分为重点新闻
file = open("highlight/19.12.8-2020.1.22.json", "w", encoding="utf-8")
for i in range(int(len(section[0])/10)):
    file.write(json.dumps(section[0][i], indent=4, ensure_ascii=False))
file.close()

file = open("highlight/1.23-2.7.json", "w", encoding="utf-8")
for i in range(int(len(section[1])/10)):
    file.write(json.dumps(section[1][i], indent=4, ensure_ascii=False))
file.close()

file = open("highlight/2.8-2.13.json", "w", encoding="utf-8")
for i in range(int(len(section[2])/10)):
    file.write(json.dumps(section[2][i], indent=4, ensure_ascii=False))
file.close()

file = open("highlight/3.10-6.25.json", "w", encoding="utf-8")
for i in range(int(len(section[3])/10)):
    file.write(json.dumps(section[3][i], indent=4, ensure_ascii=False))
file.close()






