import pandas as pd
import math as m
from round import double_round #self-written function for rounding U/delta and X_mean


def get_theta_rms(reading: float, freq: int = 1000) -> float: #works only for range = 2V
    range = 2 
    if freq < 45:
        return (1.5 * reading + 0.1 * range)/100
    if freq < 20 * 1000:
        return (0.2 * reading + 0.05 * range)/100
    if freq < 50 * 1000:
        return (1 * reading + 0.05 * range)/100
    return (3 * reading + 0.05 * range)/100

def get_theta(reading: float) -> float:
    range = 2
    return (0.015 * reading + 0.03 * range)/100

def get_theta_osc(reading: float, div: int) -> float:
    return 0.03*reading + (0.1*div + 1)/1000


filename = "СМ5-31Б_ЛР8_Поседкин_НМ_Паламарчук_АД.xlsx"
#Reading document
try:
    data = pd.read_excel(filename, header=1, index_col=0)
    print(data)
except:
    print("file not found")
    exit(0)

P = 0.95
n = 21


file = open("resultsLR8.txt", "w")

#j={current[j]}

Results = {'k, %': [i*5 for i in range(21)]} # new template dataframe purposed to export data to excel file

#print(Results)

for i in data:
    current = data[i]
    #average for multimeter
    if current.name == 'Uср м, В' or current.name == 'Uср м, В.1': 
        file.write(current.name + '\n')
        Results.update([(current.name+' X', []), (current.name+' U', [])])
        for j in current:
            theta = get_theta(j)
            U = theta / m.sqrt(3)
            Results[current.name+' U'].append(U)
            Results[current.name+' X'].append(j)
            file.write("{0}, {1}, ".format(*double_round(j, U)) + str(P) + '\n')

    #rms for multimeter 
    if current.name == 'Urms м, В' or current.name == 'Urms м, В.1': 
        file.write(current.name + '\n')
        Results.update([(current.name+' X', []), (current.name+' U', [])])
        for j in range(1, n + 1):
            theta = get_theta_rms(current[j])
            U = theta / m.sqrt(3)
            Results[current.name+' U'].append(U)
            Results[current.name+' X'].append(current[j])
            file.write("{0}, {1}, ".format(*double_round(current[j], U)) + str(P) + '\n')
    #average for oscilloscopes for sinus
    div = 14
    if current.name == 'Uср о, В': 
        file.write(current.name + '\n')
        Results.update([(current.name+' X', []), (current.name+' U', [])])
        for j in current:
            theta = get_theta_osc(j, div)
            U = theta / m.sqrt(3)
            Results[current.name+' U'].append(U)
            Results[current.name+' X'].append(j)
            file.write("{0}, {1}, ".format(*double_round(j, U)) + str(P) + '\n')
    #average for oscilloscopes for Gaussian noise
    if current.name == 'Uср о, В.1':
        file.write(current.name + '\n')
        Results.update([(current.name+' X', []), (current.name+' U', [])])
        for j in current:
            theta = get_theta_osc(j, div)
            U = theta / m.sqrt(3)
            Results[current.name+' U'].append(U)
            Results[current.name+' X'].append(j)
            file.write("{0}, {1}, ".format(*double_round(j, U)) + str(P) + '\n')
    #rms for oscilloscopes for sinus
    div = 30
    if current.name == 'Urms о, В':
        file.write(current.name + '\n')
        Results.update([(current.name+' X', []), (current.name+' U', [])])
        for j in current:
            theta = get_theta_osc(j, div)
            U = theta / m.sqrt(3)
            Results[current.name+' U'].append(U)
            Results[current.name+' X'].append(j)
            file.write("{0}, {1}, ".format(*double_round(j, U)) + str(P) + '\n')
    #rms for oscilloscopes for Gaussian noise
    if current.name == 'Urms о, В.1':
        file.write(current.name + '\n')
        Results.update([(current.name+' X', []), (current.name+' U', [])])
        for j in current:
            theta = get_theta_osc(j, div)
            U = theta / m.sqrt(3)
            Results[current.name+' U'].append(U)
            Results[current.name+' X'].append(j)
            file.write("{0}, {1}, ".format(*double_round(j, U)) + str(P) + '\n')
file.close()
    
# exporting table into .xlsx file
print([len(i) for i in Results.values()])
print(Results)

pd.DataFrame(Results).to_excel("output8.xlsx")






"""
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
data.loc['Uc'] = (data.loc['Ua'] ** 2 + data.loc['Ub'] ** 2) ** 1 / 2

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

#Exporting results in results.txt file to send Alexey
f = open(f"results{lr}.txt", "w")
for i in range(len(data.columns)):
    index = data.columns[i]
    tmp_series = data[index]
    f.write(f"U for {data.columns[i]}:\n {tmp_series['mean']},\t{tmp_series['U']},\t{P}\n")
f.close()
"""