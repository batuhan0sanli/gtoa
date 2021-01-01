# FOR MULTIPLE ANALYSIS

# ---------- GTOA.main() ARGUMENTS ----------

# -------------------------------------------
# --------- POPULATION INFORMATION ---------
# All is optional

# popSize = {int}                           - Population Size
# stopCriteria = ["it", "ev"]               - Stop criterion depends on iteration("it") or evaluation("ev")
# stopNum = {int}                           - Maximum allowed number of iterations / evaluations
# F = (1,2)                                 -
# inputSize = {int}                         -
# minLimit = {float}                        -
# maxLimit = {float}                        -
# limitless = {bool}}                       -

# --------- POPULATION INFORMATION ---------
# -------------------------------------------


# ----------------------------------
# --------- PRINT SETTINGS ---------
# All is optional
# Recommended to be all False

# writespace = False
# writeiteration = False
# writebestCand = False

# --------- PRINT SETTINGS ---------
# ----------------------------------


# ---------------------------------
# --------- SAVE CSV SETTINGS ---------
# All is optional
# Recommended to be all True

# saveCSV = True
# onlyBest = True
# csvMode = ['w', 'a']   !!!USE CAREFULLY!!! for Only This Run.

# --------- SAVE CSV SETTINGS ---------
# ---------------------------------


import GTOA
from tqdm.auto import trange
from utilities import fixLength

popSizes = [10, 20, 50]
numRun = 10

for i,popSize in zip(trange(len(popSizes), desc="Total Run     "), popSizes):
    for j in trange(numRun, desc = f'N={fixLength(popSize, 4)}        ', leave=False):
        GTOA.main(popSize=popSize, saveCSV=True, onlyBest=True, csvMode='a',
            tqdmLeave=False, tqdmDesc=f"GTOA Analysis ")

#GTOA.main(saveCSV=True, onlyBest=False, csvMode='w')
GTOA.main()