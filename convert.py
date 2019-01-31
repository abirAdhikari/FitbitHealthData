import csv
import pandas as pd

fr1=open('out.csv','rb')
data2=list(csv.reader(fr1,delimiter=','))
fr1.close()


for item2 in data2:
    if item2[12]=="Running":
        item2[12]=1
    elif item2[12]=="Cycling":
        item2[12]=7
    elif item2[12]=="Running - High pace":
        item2[12]=2
    elif item2[12]=="Cycling - Country road":
        item2[12]=8
    elif item2[12]=="Circuit training":
        item2[12]=6
    elif item2[12]=="Biking - Mountainbike":
        item2[12]=5
    elif item2[12]=="Skiing - Cross country":
        item2[12]=9
    elif item2[12]=="Running - Hills":
        item2[12]=3
    elif item2[12]=="Running - Trail":
        item2[12]=4



df2= pd.DataFrame(data2)

df2.to_csv("data.csv",sep=',')
