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

# Popülasyon Boyutu Testi
"""
popSizes = [10, 20, 30, 40, 50, 100, 200, 500, 1000]
numRun = 25

for i,popSize in zip(trange(len(popSizes), desc="Total Run     "), popSizes):
    for j in trange(numRun, desc = f'N={fixLength(popSize, 4)}        ', leave=False):
        GTOA.main(popSize=popSize, saveCSV=True, onlyBest=True, csvMode='a')

#GTOA.main(saveCSV=True, onlyBest=False, csvMode='w')
GTOA.main()
"""

# F Değeri Testi
"""
F = [1, 2]
numRun = 25
for i,Fi in zip(trange(len(F), desc="Total Run     "), F):
    for j in trange(numRun, desc = f'N={fixLength(Fi, 4)}        ', leave=False):
        GTOA.main(popSize=50, F=Fi, saveCSV=True, onlyBest=True, csvMode='a')
"""

# İyileşme Fonksiyonları Testi
numRun = 25
popSize = 50

# İyileştirme Kapalı
for j in trange(numRun, desc = f'N={fixLength("F F -", 5)}        ', leave=False):
    GTOA.main(popSize=popSize, adaptive_pen=False, half_population=False, mod=1, saveCSV=True, onlyBest=True, csvMode='a')

# Adaptive Penalty Açık Dİğeri Kapalı
for j in trange(numRun, desc = f'N={fixLength("T F -", 5)}        ', leave=False):
    GTOA.main(popSize=popSize, adaptive_pen=True, half_population=False, mod=1, saveCSV=True, onlyBest=True, csvMode='a')

# Adaptive Penalty Kapalı Dİğeri Açık 1
for j in trange(numRun, desc = f'N={fixLength("F T 1", 5)}        ', leave=False):
    GTOA.main(popSize=popSize, adaptive_pen=False, half_population=True, mod=1, saveCSV=True, onlyBest=True, csvMode='a')

# Adaptive Penalty Kapalı Dİğeri Açık 2
for j in trange(numRun, desc = f'N={fixLength("F T 2", 5)}        ', leave=False):
    GTOA.main(popSize=popSize, adaptive_pen=False, half_population=True, mod=2, saveCSV=True, onlyBest=True, csvMode='a')

# Adaptive Penalty Kapalı Dİğeri Açık 3
for j in trange(numRun, desc = f'N={fixLength("F T 3", 5)}        ', leave=False):
    GTOA.main(popSize=popSize, adaptive_pen=False, half_population=True, mod=3, saveCSV=True, onlyBest=True, csvMode='a')

