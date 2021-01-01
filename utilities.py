import copy
import random
import sys

# -----------------------------------------
# --------------- UTILITIES ---------------

# Adds up two or more lists
# Linked listeler için de çalışabilen bir fonksiyony yaz
def sumList(*args):
    if len(args) == 1: args = args[0]
    resList = [0 for i in args[0]]
    for li in args:
        for id,element in enumerate(li):
            resList[id] += element
    return resList

# Divides all the elements in the list by an integer
def divList(li, divNum):
    return [i/divNum for i in li]

# Half List
def halfList(li, popSize):
    num = popSize//2        # or num = len(li)//2  for without popSize argument
    bestList = li[:num]
    worstList = li[num:]
    return bestList, worstList

# Means up two or more lists.
def meanList(*args):
    if len(args)==1: args = args[0]
    resList = [0 for i in args[0]]
    numList = 0
    for i in args:
        resList = sumList(resList,i)
        numList += 1
    return divList(resList,numList)

# Random Choice from list. But selection is not same the key cand
def randomChoice(li, cand):
    li2 = copy.copy(li)
    li2.remove(cand)
    return random.choice(li2)

# Clip Function
def clip(li, min, max):
    def minF(x):
        if x<min: return min
        else: return x
    def maxF(x):
        if x>max: return max
        else: return x

    last = list(map(maxF, map(minF, li)))
    return last

# Fixes the length of the string
#ORTALAMA FONKSİYONU EKLE
def fixLength(str, num, placeLast=True):
    strLen = len(f"{str}")
    if strLen <= num:
        for i in range(num-strLen):
            if placeLast:
                str = f"{str}" + " "
            elif not placeLast:
                str = " " + f"{str}"
    else:
        intLen = len(f"{int(str)}")

        #Eğer 123.45 -> 4 istenmişse (123.)
        if intLen+1 == num:
            str = f"{int(str)}" + "."
        else:
            str = round(float(str),num-intLen-1)
            strLen = len(f"{str}")
            if strLen < num:
                for i in range(num - strLen):
                    if placeLast:
                        str = f"{str}" + "0"
                    elif not placeLast:
                        str = "0" + f"{str}"
    return str

"""
# Progress Bar
def update_progress(progress):
    barLength = 40 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
"""
# --------------- UTILITIES ---------------
# -----------------------------------------