import random
import utilities as ut
from user import objFunc
from tqdm.auto import tqdm
import csv

# ---------------------------------------------
# --------------- ITER FUNCTIONS ---------------

# Write CSV File
def writeCSV(li, popSize, stopNum, F, mode='w', onlyBest=True):
    name = f'stopNum={stopNum}_popSize={popSize}_F={F}'

    with open(f'results/{name}.csv', mode=mode) as csv_file:
        writer = csv.writer(csv_file)
        if onlyBest:
            writer.writerow(li)
        else:
            writer.writerows(li)
    return None

# Print for information
def information(iter, ev, pop):
    bestCand = min(pop, key = lambda x: x[-1])
    #tqdm.write(str(bestCand))
    tqdm.write("Iteration No: {}     Evalution No: {}     Best Solve: {}".format(iter, ev, bestCand[-1]))
    #tqdm.write("\n")

# Calculates the number of Iterations
def calcIterSize(stopCriteria, popSize, stopNum):
    if stopCriteria == "stit":
        return stopNum
    elif stopCriteria  == "stev":
        return (stopNum - popSize) // (2*popSize + 1)

# Clip for iteration
def iterationClip(cand, minLimit, maxLimit, limitless):
    if limitless:
        return cand
    else:
        return ut.clip(cand, minLimit, maxLimit)

# Calculates the number of stop criteria number for Step 2
def stopNumCalcFirst(stopCriteria, popSize):
    if stopCriteria == "stit":
        return 0
    elif stopCriteria == "stev":
        return popSize
    else:
        raise Exception("stopCriteria can be ONLY 'it' or 'ev'")

# Calculates the number of stop criteria number for Step 8
def stopNumCalc(stopCriteria, popSize):
    if stopCriteria == "it":
        return 1
    elif stopCriteria == "ev":
        return 2*popSize + 1
    else:
        raise Exception("stopCriteria can be ONLY 'it' or 'ev'")

# Choose Best
def chooseCand(cand1, cand2):
    if cand1[-1] < cand2[-1]:       # If candidate 1 better than candidate 2 (Lower is better)
        return cand1
    else:
        return cand2

# First Population (Last column is 0 for Objective Function) (Step 1)
def firstPop(inputSize, popSize, minLimit, maxLimit):
    return [[random.uniform(minLimit, maxLimit) for i in range(inputSize)] + [0] for j in range(popSize)]

# Evaluate the population. Including all candidate.
def evaluatePop(pop):
    for cand in pop:
        cand[-1] = objFunc(cand[:-1])
    return pop

# Evaluate the candidate. ONLY one candidate. ("cand" be a list)
def evaluateCand(cand):
    cand[-1] = objFunc(cand[:-1])
    return cand

# Teacher Allocation - Want a SORTED population list (Step 4)
def teacherAllo(sortedPop):
    cand1 = sortedPop[0]
    cand2 = ut.meanList(sortedPop[0], sortedPop[1], sortedPop[2])  #  Three best individuals are selected and averaged
    cand2 = evaluateCand(cand2)     # Evalueted candidate
    return chooseCand(cand1, cand2)

# (Step 6.1.1)
def teachPhaseBest(pop, teacher, F, minLimit, maxLimit, limitless):
    # Random Numbers

    #c = 1-b

    # Mean of Class
    mean = ut.meanList(pop)

    newPop = []
    for cand in pop:
        newCand = []
        for i_cand, i_mean, i_teacher in zip(cand[:-1], mean[:-1], teacher[:-1]):
            a, b = random.random(), random.random()
            newProp = i_cand + a*(i_teacher - F*(b*i_mean + (1-b)*i_cand))
            newCand.append(newProp)

        # Clip
        newCand = iterationClip(newCand, minLimit, maxLimit, limitless)
        newCand = evaluateCand(newCand + [0])
        newPop.append(chooseCand(cand, newCand))
    return newPop

# (Step 6.1.2, Step 6.2.2)
def studentPhase(pop, oldPop, minLimit, maxLimit, limitless):
    # Random Numbers

    newPop = []

    for cand, oldCand in zip(pop, oldPop):
        newCand = []
        randStu = ut.randomChoice(pop,cand)
        i_am_good = True if cand[-1] < randStu[-1] else False
        for i_cand, i_oldCand, i_randStu in zip(cand[:-1], oldCand[:-1], randStu[:-1]):
            e, g = random.random(), random.random()
            if i_am_good:
                newProp = i_cand + e * (i_cand - i_randStu) + g * (i_cand - i_oldCand)
            else:
                newProp = i_cand - e * (i_cand - i_randStu) + g * (i_cand - i_oldCand)
            newCand.append(newProp)

        # Clip
        newCand = iterationClip(newCand, minLimit, maxLimit, limitless)
        newCand = evaluateCand(newCand + [0])
        newPop.append(chooseCand(cand, newCand))
    return newPop

# (Step 6.2.1)
def teachPhaseWorst(pop, teacher, minLimit, maxLimit, limitless):
    # Random Numbers


    newPop = []
    for cand in pop:
        newCand = []
        for i_cand, i_teacher in zip(cand[:-1], teacher[:-1]):
            d = random.random()
            newProp = i_cand + 2*d*(i_teacher - i_cand)
            newCand.append(newProp)

        # Clip
        newCand = iterationClip(newCand, minLimit, maxLimit, limitless)
        newCand = evaluateCand(newCand + [0])
        newPop.append(chooseCand(cand, newCand))
    return newPop

# --------------- ITER FUNCTIONS ---------------
# ---------------------------------------------