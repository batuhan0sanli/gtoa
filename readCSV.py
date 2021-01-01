import csv
import os
from statistics import mean
from utilities import fixLength

stopNum = 25000
F = 1
popSizes = []

os.chdir(os.getcwd() + "/results")

# PopSizes List
for iCsv in os.listdir():
    if "stopNum" in iCsv:
        for prop in iCsv.split("_"):
            key, val = prop.split("=")
            if key == "popSize":
                popSizes.append(int(val))
popSizes.sort()


# Read Csv
print()
print(f"                         {stopNum} Analiz için değerler                       ")
print("|    Pop Size    |    Best Value    |    Mean Value    |    Worst Value    |")
print("----------------------------------------------------------------------------")
for popSize in popSizes:
    name = f"stopNum={stopNum}_popSize={popSize}_F={F}.csv"
    temp = []
    with open(name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i in csv_reader:
            temp.append(float(i[-1]))
    best_val = min(temp)
    mean_val = mean(temp)
    worst_val = max(temp)
    print(f"|    {fixLength(popSize, 8)}    |    {fixLength(best_val,10)}    |    {fixLength(mean_val,10)}    |    {fixLength(worst_val,11)}    |")