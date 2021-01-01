# FOR SINGLE ANALYSIS

import user
import iterFunctions as ifunc
import utilities as ut
import copy



# ---------------------------------------------
# --------------- MAIN FUNCTION ---------------
def main(popSize=user.popSize, stopCriteria=user.stopCriteria , stopNum=user.stopNum, F=user.F, inputSize=user.inputSize,
         minLimit=user.minLimit, maxLimit=user.maxLimit, limitless=user.limitless,
         printSpace=False, printIteration=False, printBestCand=False,
         saveCSV=False, onlyBest=True, csvMode='a',
         tqdmLeave=True, tqdmDesc=''):

    # Step a: Information Termination Criteria
    iterSize = ifunc.calcIterSize(stopCriteria, popSize, stopNum)
    currentNum = 0
    iter = 0
    ev = copy.copy(popSize)

    # Step 1: Initialization information
    pop = ifunc.firstPop(inputSize, popSize, minLimit, maxLimit)

    # Step 2: Population evaluation
    pop = ifunc.evaluatePop(pop)
    #currentNum += ifunc.stopNumCalcFirst(stopCriteria, popSize)
    #ifunc.information(iter, ev, pop)

    # Step 3: Termination criteria
    for i in range(iterSize):
        # Step 4: Teacher allocation phase
        pop.sort(key=lambda x: x[-1])  # Pop List is sorting.
        teacher = ifunc.teacherAllo(pop)

        # Step 5: Ability grouping phase
        bestGroup, worstGroup = ut.halfList(pop, popSize)

        # Step 6.1.1: Teacher Phase for Best Group
        newBestGroup = ifunc.teachPhaseBest(bestGroup, teacher, F, minLimit, maxLimit, limitless)

        # Step 6.1.2: Student Phase for Best Group
        lastBestGroup = ifunc.studentPhase(newBestGroup, bestGroup, minLimit, maxLimit, limitless)

        # Step 6.2.1: Teacher Phase for Worst Group
        newWorstGroup = ifunc.teachPhaseWorst(worstGroup, teacher, minLimit, maxLimit, limitless)

        # Step 6.2.2: Student Phase for Best Group
        lastWorstGroup = ifunc.studentPhase(newWorstGroup, worstGroup, minLimit, maxLimit, limitless)

        # Step 7: Construct population
        pop = lastBestGroup + lastWorstGroup

        # Step 8: Population evaluation
        #currentNum += ifunc.stopNumCalc(stopCriteria, popSize)

        # Step c: Print information
        iter += 1
        ev += 2 * popSize + 1
        #ifunc.information(iter, ev, pop)

        # Step d: Configure kwargs
        bestCand = min(pop, key=lambda x: x[-1])

        # Print Settings
        if printSpace:
            print("")

        if printIteration:
            print("Iteration No: {}     Evalution No: {}     Best Solve: {}".format(iter, ev, bestCand[-1]))

        if printBestCand:
            print(str(bestCand))
    # Sace CSV Settings
    if saveCSV:
        if onlyBest:
            ifunc.writeCSV(bestCand, popSize, stopNum, F, mode=csvMode, onlyBest=onlyBest)
        else:
            ifunc.writeCSV(pop, popSize, stopNum, F, mode=csvMode, onlyBest=onlyBest)
# --------------- MAIN FUNCTION ---------------
# ---------------------------------------------


if __name__ == '__main__':
    print("WARNING! ONLY SINGLE ANALYSIS \n")
    main(printBestCand=False, printIteration=True)