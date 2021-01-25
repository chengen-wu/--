# coding=utf-8

import xlrd
import pandas
import xlwt
import numpy
import matplotlib.pyplot as plt

# 我们应用每天新增病例数与不同情绪的每天频数与频率进行相关性检验

# 打开两个表格文件
data1 = xlrd.open_workbook('final.xls')
table1=data1.sheet_by_name("sheet 1")
data2 = xlrd.open_workbook("新增数据.xlsx")
table2=data2.sheet_by_name("Sheet1")

# 获取情绪的频数
emotion=[]
for i in range(8):
    emotion.append([])
    for j in range(88):
        emotion[i].append(table1.cell(1+i,j+51).value)
emotion.append([])
for i in range(88):
    emotion[8].append(emotion[0][i]+emotion[1][i]+emotion[2][i]+emotion[3][i]+emotion[4][i]+emotion[5][i]+emotion[6][i]+emotion[7][i])

# 情绪每天占的频率
emotionRate=[]
for i in range(8):
    emotionRate.append([])
    for j in range(88):
        emotionRate[i].append(emotion[i][j]/emotion[8][j])

# 每日的新增数
newlyIncreaseOfAcquire=[]
for i in range(88):
    newlyIncreaseOfAcquire.append(table2.cell(1,i+1).value)

# 在后续的计算中我们发现了在2020-02-12那天的新增数为15152，在后续拟合中为异常点，我们舍弃不要
for i in range(len(newlyIncreaseOfAcquire)):
    if newlyIncreaseOfAcquire[i]==15152:
        newlyIncreaseOfAcquire.pop(i)
        for j in range(8):
            emotion[j].pop(i)
            emotionRate[j].pop(i)
        break

# 相关系数的计算--频数
relationship=[]
newlyIncreaseOfAcquire_s=pandas.Series(newlyIncreaseOfAcquire)
for i in range(8):
    relationship.append(newlyIncreaseOfAcquire_s.corr(pandas.Series(emotion[i])))
print(relationship)

# 相关系数计算--频率
relationshipOfEmotionRate=[]
newlyIncreaseOfAcquire_s=pandas.Series(newlyIncreaseOfAcquire)
for i in range(8):
    relationshipOfEmotionRate.append(newlyIncreaseOfAcquire_s.corr(pandas.Series(emotionRate[i])))
print("相关系数为")
print(relationshipOfEmotionRate)

#创建焦虑频率和每日新增的表格
workbook =xlwt.Workbook(encoding ="utf-8",style_compression=0)
sheet =workbook.add_sheet("Sheet1",cell_overwrite_ok=True)  #Cell_overwirte_ok 是能够覆盖单元表格的意思。
for i in range(len(emotionRate[4])):
    sheet.write(i,0,emotionRate[4][i])
for i in range(len(newlyIncreaseOfAcquire)):
    sheet.write(i,1,newlyIncreaseOfAcquire[i])
workbook.save("散点图数据.xls")

# 一次线性拟合
x=numpy.array(newlyIncreaseOfAcquire)
y=numpy.array(emotionRate[4])
f=numpy.polyfit(x,y,1)
print("焦虑占比与每日新增函数为")
print(f)

p =numpy.poly1d(f)
yvals = p(x)  #拟合y值

#绘图
plot1 = plt.plot(x, y, 's',label='original values')
plot2 = plt.plot(x, yvals, 'r',label='polyfit values')
plt.xlabel('x')
plt.ylabel('y')
plt.legend(loc=4) #指定legend的位置右下角
plt.title('polyfitting')
plt.show()







