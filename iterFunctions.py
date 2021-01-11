import random
import utilities as ut
from user import objFunc
from tqdm.auto import tqdm
import csv

# ---------------------------------------------
# --------------- ITER FUNCTIONS ---------------

# Write CSV File
def writeCSV(li, popSize, stopCriteria, stopNum, F, adaptive_pen, half_population, mod, mode='w', onlyBest=True):
    name = f'stop={stopNum}{stopCriteria}__pSize={popSize}__F={F}__aPen={adaptive_pen}__hPop={half_population}__hfMod={mod}'

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
def calcIterSize(isIteration, popSize, stopNum):
    if isIteration:
        return stopNum
    else:
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
def evaluatePop(pop, iter, adaptive_pen):
    if adaptive_pen:
        for cand in pop:
            cand[-1] = objFunc(cand[:-1], iter)
    else:
        for cand in pop:
            cand[-1] = objFunc(cand[:-1])
    return pop

# Evaluate the candidate. ONLY one candidate. ("cand" be a list)
def evaluateCand(cand, iter, adaptive_pen):
    if adaptive_pen: cand[-1] = objFunc(cand[:-1], iter)
    else: cand[-1] = objFunc(cand[:-1])
    return cand

# Teacher Allocation - Want a SORTED population list (Step 4)
def teacherAllo(sortedPop, iter, adaptive_pen):
    cand1 = sortedPop[0]
    cand2 = ut.meanList(sortedPop[0], sortedPop[1], sortedPop[2])  #  Three best individuals are selected and averaged
    cand2 = evaluateCand(cand2, iter, adaptive_pen)     # Evalueted candidate
    return chooseCand(cand1, cand2)

# (Step 6.1.1)
def teachPhaseBest(pop, teacher, F, minLimit, maxLimit, limitless, iter, adaptive_pen):
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
        newCand = evaluateCand(newCand + [0], iter, adaptive_pen)
        newPop.append(chooseCand(cand, newCand))
    return newPop

# (Step 6.1.2, Step 6.2.2)
def studentPhase(pop, oldPop, minLimit, maxLimit, limitless, iter, adaptive_pen):
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
        newCand = evaluateCand(newCand + [0], iter, adaptive_pen)
        newPop.append(chooseCand(cand, newCand))
    return newPop

# (Step 6.2.1)
def teachPhaseWorst(pop, teacher, minLimit, maxLimit, limitless, iter, adaptive_pen):
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
        newCand = evaluateCand(newCand + [0], iter, adaptive_pen)
        newPop.append(chooseCand(cand, newCand))
    return newPop

# It decides whether the iterations will continue or not for Static Termination
def staticTerm(isIter, cur_iter, cur_ev, stopNum, one_it_an):
    # Static Iteration Termination
    if isIter:
        if cur_iter >= stopNum: return True

    # Static Evaluation Termination
    else:
        if cur_ev + one_it_an >= stopNum + 1: return True
    return False

# Evaluation to Iteration
def ev2it(ev, popSize):
    ev = ev - popSize
    return ev // (2*popSize + 1)


# It decides whether the iterations will continue or not for Dynamic Termination
def dynamicTerm(isIter, bestCandList, impRate, stopNum, popSize):
    # Eğer analiz bazlı çalışıyor ise
    if not isIter:
        stopNum = ev2it(stopNum, popSize)

    oldCand = bestCandList[-stopNum]
    newCand = bestCandList[-1]

    if oldCand * (1 - impRate) < newCand: return True
    else: return False

# Controls the population division requirement
def halfPopQ(isIter, stopNum, halfPopPercent, halfPopImpRate, popSize, bestCandList, halfPopCount):
    # Eğer iterasyon bazlı çalışıyor ise
    if isIter:
        countLim = round(stopNum * halfPopPercent)  # Sondan kaçıncı elemanın indexi olduğu

    # Eğer analiz bazlı çalışıyor ise
    else:
        countLim = round(ev2it(stopNum, popSize) * halfPopPercent)  # Sondan kaçıncı elemanın indexi olduğu

    # Yeteri kadar iterasyon yapılmışsa
    if halfPopCount >= countLim:
        oldCand = bestCandList[-countLim]
        newCand = bestCandList[-1]

        # Yeni aday "halfPopImpRate" oranında eski adaydan daha iyiyse
        if oldCand * (1 - halfPopImpRate) < newCand:
            return True
        else:
            return False
    else:
        return False
# --------------- ITER FUNCTIONS ---------------
# ---------------------------------------------