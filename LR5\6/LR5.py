import pandas as pd
import math as m
from round import double_round #self-written function for rounding U/delta and X_mean


lr = "LR6"
filename = "/home/nik/code/PythonProjects/LR5\\6/СМ5_31Б_ЛР6_Поседкин_НМ_Паламарчук_АД.xlsx"

#Reading document
try:
    data = pd.read_excel(filename, header=2, index_col=0)
except:
    print("File not found")
    exit(0)

P = 0.95
Theta = {'U': 0, 't': 0}
n = 20

#Adding mean, Ua as raws for each column
data.loc['mean'] = data.mean()
data.loc['Ua'] = data.std() / m.sqrt(n)

#Initializing Ub as raw
data.loc['Ub'] = 0

#Calculating Ub for U, B
data.loc['Ub']['U, В'] = Theta['U'] / m.sqrt(3)
for i in range(1, 8):
    data.loc['Ub']['U, В.' + str(i)] = Theta['U'] / m.sqrt(3)

# for h, %
data.loc['Ub']['h, %'] = (Theta['U'] / m.sqrt(3)) * 100
for i in range(1, 8):
    data.loc['Ub']['h, %.' + str(i)] = (Theta['U'] / m.sqrt(3)) * 100

#Calculating Uc
data.loc['Uc'] = (data.loc['Ua'] ** 2 + data.loc['Ub'] ** 2) ** (1 / 2)

#Calculating U by formula U = k*Uc
#For P = 0,95 k = 2
k = 2
data.loc['U'] = k * data.loc['Uc']

#Printing results
print(data.columns, len(data.columns))
for i in range(len(data.columns)):
    index = data.columns[i]
    tmp_series = data[index]
    print(f"U for {data.columns[i]}:\n {tmp_series['mean']},\t{tmp_series['U']},\t{P}")

#Exporting results in results.txt file
f = open(f"results{lr}.txt", "w")
for i in range(len(data.columns)):
    index = data.columns[i]
    tmp_series = data[index]
    x, U = double_round(tmp_series['mean'], tmp_series['U'])
    f.write(f"U for {data.columns[i]}:\n {x},\t{U},\t{P}\n")
#Closing file
f.close()
