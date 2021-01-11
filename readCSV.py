import csv
import os
from statistics import mean
from utilities import fixLength

stopNum = 20000
F = 1
popSizes = [50]

os.chdir(os.getcwd() + "/results")

# PopSizes List
for iCsv in os.listdir():
    if "stopNum" in iCsv:
        for prop in iCsv.split("__"):
            key, val = prop.split("=")
            if key == "popSize":
                popSizes.append(int(val))
popSizes.sort()

stopCriteria = "stev"
adaptive_pen = "False"
half_population = "True"
mod = "3"

# Read Csv
print()
print(f"                         {stopNum} Analiz için değerler                       ")
print("|    Pop Size    |    Best Value    |    Mean Value    |    Worst Value    |")
print("----------------------------------------------------------------------------")
for popSize in popSizes:
    name = f'stop={stopNum}{stopCriteria}__pSize={popSize}__F={F}__aPen={adaptive_pen}__hPop={half_population}__hfMod={mod}.csv'
    temp = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i in csv_reader:
            temp.append(float(i[-1]))
    best_val = min(temp)
    mean_val = mean(temp)
    worst_val = max(temp)
    print(f"|    {fixLength(popSize, 8)}    |    {fixLength(best_val,10)}    |    {fixLength(mean_val,10)}    |    {fixLength(worst_val,11)}    |")