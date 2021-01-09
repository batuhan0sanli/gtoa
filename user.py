from objectiveFunction import objectiveFunction

# ------------------------------------
# --------------- USER ---------------

# Popülasyon Boyutu
popSize = 100

# Durdurma kriterinin iterasyon mu yoksa analiz bazlı mı çalışılacağı
# (static iteration, static evaluation, dynamic iteration, dynamic evaluation) ("stit", "stev", "dyit" "dyev")
# Son n analizde %0.1'den daha az iyileşme olursa dur
stopCriteria = "dyit"

# Maksimum izin verilen iterasyon / analiz sayısı  /  maksimum iyileşme olmadan izin verilen iterasyon / analiz sayısı
stopNum = 300

# İstenen İyileşme oranı
impRate = 0.0001

# F değeri (öğretim faktörü) (1 veya 2 seçilebilir)
F = 1

# Optimize edilecek girdi sayısı
inputSize = 10

# Sınır değerleri
# Eğer sınır yok ise bu sınırlar başlangıç popülasyonu için girilmelidir.
minLimit, maxLimit = 0.1, 35

# Sınır yok mu?
limitless = False


# --------------- IMPROVEMENTS ---------------
# --------------------------------------------

# --- Adaptive Penalty ---
# Ceza'nın önemi iterasyon ilerledikçe yükselsin mi?
adaptive_pen = True

# Amaç fonksiyonunda Ceza Katsayısı
# Default 1
factor = 1


# --- Dividing the Population in Half ---
# Popülasyonu yarıya bölme geliştirmesi aktif olsun mu?
half_population = True

# Aranan iyileşme oranı
halfPopImpRate = impRate

# Son <halfPopPercent>*stopNum analizde iyileşme olmazsa yarıya düşürsün
halfPopPercent = 0.2

# Mod Seçimi (Detaylı bilgi için blz. adaptive_ideas/halfPopulation.py)
mod = 1

# Popülasyon kaç aday'ın altına düştüğünde yarıya düşürme işlemi yapılmasın?
lowerLim = 5

# Mod 2 / Mod 3 => Seçilecek en iyi / en kötü adayların yüzdesi
sel_percent = 0.2

# --------------------------------------------
# --------------- IMPROVEMENTS ---------------



# Amaç fonksiyonu - Objective Function (girdiler liste içerisinde verilmelidir)
def objFunc(alan, iter=stopNum, factor=factor, iter_div=stopNum):
    return objectiveFunction(alan, size10bar2D, factor, iter, iter_div)


# ----- 10-bar Planar Cantilever -----
# solution by Mustafa Sonmez, Artificial Bee Colony algorithm for optimization of truss structures, 2011
size10bar2D=[
    [10000.0,0.1],
    [[1,0.0,0.0],[2,0.0,360.0],[3,360.0,0.0],[4,360.0,360.0],[5,720.0,0.0],[6,720.0,360.0]],
    [[1,1,1],[2,1,1]],
    [30.548,0.1,23.18,15.218,0.1,0.551,7.463,21.058,21.501,0.1],
    [[1,1,2,4],[2,2,4,6],[3,3,1,3],[4,4,3,5],[5,5,3,4],[6,6,5,6],[7,7,2,3],[8,8,1,4],[9,9,4,5],[10,10,3,6]],
    [
        [[3,0.0,-100.0],[5,0.0,-100.0]]
    ]
]
# ------------------------------------

# --------------- USER ---------------
# ------------------------------------


