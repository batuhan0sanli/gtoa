import objectiveFunction as obj

# ------------------------------------
# --------------- USER ---------------

# Popülasyon Boyutu
popSize = 20

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

# Amaç fonksiyonu - Objective Function (girdiler liste içerisinde verilmelidir)
def objFunc(x):
    return obj.objectiveFunction(x, obj.size10bar2D)



# --------------- USER ---------------
# ------------------------------------

