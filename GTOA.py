# FOR SINGLE ANALYSIS

import user
import iterFunctions as ifunc
import utilities as ut
import copy
import adaptive_ideas.halfPopulation as hP


# ---------------------------------------------
# --------------- MAIN FUNCTION ---------------
def main(popSize=user.popSize, stopCriteria=user.stopCriteria, stopNum=user.stopNum, impRate=user.impRate, F=user.F,
         inputSize=user.inputSize, minLimit=user.minLimit, maxLimit=user.maxLimit, limitless=user.limitless,
         adaptive_pen=user.adaptive_pen,
         half_population=user.half_population, halfPopImpRate=user.halfPopImpRate, halfPopPercent=user.halfPopPercent, mod=user.mod, lowerLim=user.lowerLim, sel_percent=user.sel_percent,
         printSpace=False, printIteration=False, printBestCand=False,
         saveCSV=False, onlyBest=True, csvMode='a'):

    # Step a: Dictionary
    prop = {}

    prop["isStatic"] = True if stopCriteria[:2] == "st" else False      # static -> True    | dynamic -> False
    prop["isIteration"] = True if stopCriteria[2:] == "it" else False   # iteration -> True | evaluation -> False

    # Step b: Information Termination Criteria
    """
    if prop["isStatic"]:        # For Static
        if prop["isIteration"]:
        max_iter = ifunc.calcIterSize(prop["isIteration"], popSize, stopNum)    # Maksimum izin verilen iterasyon

    else:                       # For Dynamic
        max_noImp = ifunc.calcIterSize(prop["isIteration"], popSize, stopNum)   # Maksimum iyileşmesiz izin verilen iterasyon
        prop["termQ"] = False   # max_noImp sayısına ulaşmadan sorgu yapılmamasını sağlar.
    """
    prop["termQ"] = False   # max_noImp sayısına ulaşmadan sorgu yapılmamasını sağlar.
    iter = 0
    ev = copy.copy(popSize)
    halfPopCount = 0

    # Step 1: Initialization information
    pop = ifunc.firstPop(inputSize, popSize, minLimit, maxLimit)

    # Step 2: Population evaluation
    pop = ifunc.evaluatePop(pop, iter, adaptive_pen)

    # Dynamic Termination - Best Cand List
    bestCandList = []


    while True:
        one_it_an = 2 * len(pop) + 1   # Bir iterasyonda kaç analiz yapıldığının bilgisidir. Popülasyon değişebileceğinden her iterasyonda tekrar hesaplanır.
        # Step 4: Teacher allocation phase
        pop.sort(key=lambda x: x[-1])  # Pop List is sorting.
        teacher = ifunc.teacherAllo(pop, iter, adaptive_pen)

        # Step 5: Ability grouping phase
        bestGroup, worstGroup = ut.halfList(pop, popSize)

        # Step 6.1.1: Teacher Phase for Best Group
        newBestGroup = ifunc.teachPhaseBest(bestGroup, teacher, F, minLimit, maxLimit, limitless, iter, adaptive_pen)

        # Step 6.1.2: Student Phase for Best Group
        lastBestGroup = ifunc.studentPhase(newBestGroup, bestGroup, minLimit, maxLimit, limitless, iter, adaptive_pen)

        # Step 6.2.1: Teacher Phase for Worst Group
        newWorstGroup = ifunc.teachPhaseWorst(worstGroup, teacher, minLimit, maxLimit, limitless, iter, adaptive_pen)

        # Step 6.2.2: Student Phase for Best Group
        lastWorstGroup = ifunc.studentPhase(newWorstGroup, worstGroup, minLimit, maxLimit, limitless, iter, adaptive_pen)

        # Step 7: Construct population
        pop = lastBestGroup + lastWorstGroup

        # Step c: Print information
        iter += 1
        ev += one_it_an
        halfPopCount += 1

        # Step d: Select Best Candidate - Append to bestCandList
        bestCand = min(pop, key=lambda x: x[-1])
        bestCandList.append(bestCand[-1])

        # Print Settings
        if printSpace:
            print("")

        if printIteration:
            print(f"Iteration No: {iter}    Evaluation No: {ev}    Length Pop: {len(pop)}    Best Solve: {bestCand[-1]}")

        if printBestCand:
            print(str(bestCand))


        # TERMINATION
        # Dynamic Termination - Edit TermQ
        if not prop["termQ"]:
            if prop["isIteration"]:
                if iter == stopNum: prop["termQ"] = True
            else:
                if ev >= stopNum: prop["termQ"] = True

        # Static Termination
        if prop["isStatic"] and ifunc.staticTerm(prop["isIteration"], iter, ev, stopNum, one_it_an):
            break

        # Dynamic Termination
        else:
            if prop["termQ"]:
                if ifunc.dynamicTerm(prop["isIteration"], bestCandList, impRate, stopNum, popSize):
                    break


        # Dividing the Population in Half
        # Eğer Popülasyonu ikiye bölme işlemi açıksa
        if half_population:

            # Eğer şartlar sağlanıyorsa
            if ifunc.halfPopQ(prop["isIteration"], stopNum, halfPopPercent, halfPopImpRate, popSize, bestCandList, halfPopCount):
                pop = hP.halfPop(pop, mod, lowerLim, sel_percent)
                halfPopCount = 0

    # Save CSV Settings
    if saveCSV:
        if onlyBest:
            ifunc.writeCSV(bestCand, popSize, stopCriteria, stopNum, F, adaptive_pen, half_population, mod, mode=csvMode, onlyBest=onlyBest)
        else:
            ifunc.writeCSV(pop, popSize, stopCriteria, stopNum, F, mode=csvMode, onlyBest=onlyBest)
    return pop
# --------------- MAIN FUNCTION ---------------
# ---------------------------------------------



if __name__ == '__main__':
    print("WARNING! ONLY SINGLE ANALYSIS \n")
    main(printBestCand=False, printIteration=True)