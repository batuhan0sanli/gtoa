import random
import utilities as ut
from user import objFunc
import csv

# ---------------------------------------------
# --------------- ITER FUNCTIONS ---------------
# Write CSV File
def writeCSV(li, popSize, stopCriteria, stopNum, F, adaptive_pen, half_population, mod=0, mode='w', onlyBest=True):
    """
    Popülasyon sonunda CSV dosyalarını kaydetmeye yarar.
    Proje klasöründe 'results/' klasörü oluşturulmuş olmalıdır. Dosya ismi aşağıdaki şekildedir:
    stop={stopNum}{stopCriteria}__pSize={popSize}__F={F}__aPen={adaptive_pen}__hPop={half_population}__hfMod={mod}.csv

    Zorunlu argümanlar:
    li:                 Yazdırılması istenen aday/adaylar (list)
    popSize:            Başlangıçta tercih edilen popülasyon büyüklüğü (int)
    stopCriteria:       Durdurma kriteri (str)
    stopNum:            Durdurma sayısı (int)
    F:                  Öğrenme katsayısı / F değeri (int)
    adaptive_pen:       Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    half_population:    Popülasyonu yarıya düşürme iyileşmesinin aktif olma durumu (bool)

    Opsiyonel argümanlar:
    mod:                Popülasyonu yarıya düşürme iyileştirmesinde tercih edilen mod [1, 2, 3]
    mode:               CSV kaydında tercih edilecek kayıt modu ['a', 'w' ..]
    onlyBest:           Sadece tek bir aday yazdırma seçeneği. (bool)
                        Eğer kapatılırsa li içerisindeki her eleman CSV dosyasında bir alt satıra yazılır.
    """
    name = f'stop={stopNum}{stopCriteria}__pSize={popSize}__F={F}__aPen={adaptive_pen}__hPop={half_population}__hfMod={mod}'

    with open(f'results/{name}.csv', mode=mode) as csv_file:
        writer = csv.writer(csv_file)
        if onlyBest:
            writer.writerow(li)
        else:
            writer.writerows(li)
    return None


# Clip for iteration
def iterationClip(cand, minLimit, maxLimit, limitless):
    """
    Adayın limitless değerine göre clip edilip edilmeyeceğine karar verir ve gerekliyse clip edip döndürür.
    Gerekli değil ise clip edilmemiş halini döndürür.

    Zorunlu Argümanlar:
    cand:       Adayın kendisi (list)
    minLimit:   İstenen minimum değer (int or float)
    maxLimit:   İstenen maximum değer (int or float)
    limitless:  Adayın alabileceği değerlerin sınırsız olduğunu söyler (bool)
    """
    if limitless:
        return cand
    else:
        return ut.clip(cand, minLimit, maxLimit)


# Choose Best
def chooseCand(cand1, cand2):
    """
    Verilen iki aday arasından daha iyi olanı (son elemanı daha düşük olanı) döndürür

    Zorunlu argümanlar:
    cand1:  Karşılaştırılacak adaylardan ilki (list)
    cand2:  Karşılaştırılacak adaylardan ikincisi (list)
    """
    if cand1[-1] < cand2[-1]:       # If candidate 1 better than candidate 2 (Lower is better)
        return cand1
    else:
        return cand2


# First Population (Last column is 0 for Objective Function) (Step 1)
def firstPop(inputSize, popSize, minLimit, maxLimit):
    """
    İlk popülasyonu üretir.

    Zorunlu argümanlar:
    inputSize:  Tasarım değişkeni sayısı (int)
    popSize:    Başlangıçta tercih edilen popülasyon büyüklüğü (int)
    minLimit:   İstenen minimum değer (int or float)
    maxLimit:   İstenen maximum değer (int or float)
    """
    return [[random.uniform(minLimit, maxLimit) for i in range(inputSize)] + [0] for j in range(popSize)]


# Evaluate the population. Including all candidate.
def evaluatePop(pop, iter, adaptive_pen):
    """
    Popülasyondaki tüm adayları değerlendirir ve değerlendirme sonucunu son elemanına yazılmış bir şekilde döndürür.

    Zorunlu argümanlar:
    pop:            Popülasyon listesi (list)
    iter:           Adaptif ceza iyileştirmesi için iterasyon numarası (int)
    adaptive_pen:   Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    """
    return [evaluateCand(cand, iter, adaptive_pen) for cand in pop]


# Evaluate the candidate. ONLY one candidate. ("cand" be a list)
def evaluateCand(cand, iter, adaptive_pen):
    """
    Tek bir aday değerlendirilir ve değerlendirme sonucunu son elemanına yazılmış bir şekilde döndürür.

    Zorunlu argümanlar:
    pop:            Popülasyon listesi (list)
    iter:           Adaptif ceza iyileştirmesi için iterasyon numarası (int)
    adaptive_pen:   Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    """
    if adaptive_pen: cand[-1] = objFunc(cand[:-1], iter)
    else: cand[-1] = objFunc(cand[:-1])
    return cand


# Teacher Allocation - Want a SORTED population list (Step 4)
def teacherAllo(sortedPop, iter, adaptive_pen):
    """
    Öğretmen belirleme aşaması için öğretmeni seçer ve döndürür.

    Zorunlu argümanlar:
    sortedPop:  İyiden kötüye doğru sıralanmış popülasyon listesi (list)
    iter:           Adaptif ceza iyileştirmesi için iterasyon numarası (int)
    adaptive_pen:   Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    """
    cand1 = sortedPop[0]
    cand2 = ut.meanList(sortedPop[0], sortedPop[1], sortedPop[2])  #  Three best individuals are selected and averaged
    cand2 = evaluateCand(cand2, iter, adaptive_pen)     # Evalueted candidate
    return chooseCand(cand1, cand2)


# (Step 6.1.1)
def teachPhaseBest(pop, teacher, F, minLimit, maxLimit, limitless, iter, adaptive_pen):
    """
    İyi sınıf öğretmen aşaması için bir sonraki popülasyonu hazırlar.

    Zorunlu argümanlar:
    pop:        Popülasyon (nested list)
    teacher:    Öğretmen (list)
    F:                  Öğrenme katsayısı / F değeri (int)
    minLimit:   İstenen minimum değer (int or float)
    maxLimit:   İstenen maximum değer (int or float)
    limitless:  Adayın alabileceği değerlerin sınırsız olduğunu söyler (bool)
    iter:           Adaptif ceza iyileştirmesi için iterasyon numarası (int)
    adaptive_pen:   Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    """
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
    """
    Hem iyi hem de kötü sınıf öğrenci aşaması için bir sonraki popülasyonu hazırlar.

    Zorunlu argümanlar:
    pop:        Öğretmen aşamasından gelen popülasyon (nested list)
    oldPop:        Öğretmen aşamasından önceki popülasyon (nested list)
    minLimit:   İstenen minimum değer (int or float)
    maxLimit:   İstenen maximum değer (int or float)
    limitless:  Adayın alabileceği değerlerin sınırsız olduğunu söyler (bool)
    iter:           Adaptif ceza iyileştirmesi için iterasyon numarası (int)
    adaptive_pen:   Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    """
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
    """
    Kötü sınıf öğretmen aşaması için bir sonraki popülasyonu hazırlar.

    Zorunlu argümanlar:
    pop:        Popülasyon (nested list)
    teacher:    Öğretmen (list)
    minLimit:   İstenen minimum değer (int or float)
    maxLimit:   İstenen maximum değer (int or float)
    limitless:  Adayın alabileceği değerlerin sınırsız olduğunu söyler (bool)
    iter:           Adaptif ceza iyileştirmesi için iterasyon numarası (int)
    adaptive_pen:   Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
    """
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


# Evaluation to Iteration
def ev2it(ev, popSize):
    """
    Analiz sayısını iterasyon sayısına dönüştürür.

    Zorunlu argümanlar:
    ev:         Çevrilmek istenen analiz sayısı (int)
    popSize:    Popülasyon boyutu (int)
    """
    ev = ev - popSize
    return ev // (2*popSize + 1)


# It decides whether the iterations will continue or not for Static Termination
def staticTerm(isIter, cur_iter, cur_ev, stopNum, one_it_an):
    """
    Statik sonlandırmanın olup olmayacağına karar verir. Bool döndürür.

    Zorunlu argümanlar:
    isIter:     Sonlandırmanın iterasyon bazlı olup omadığı (bool)
    cur_iter:   İterasyon numarası (int)
    cur_ev:     Şu ana kadar yapılan analiz miktarı (int)
    stopNum:    Durdurma sayısı (int)
    one_it_an:  Bir iterasyondaki analiz sayısı
    """
    # Static Iteration Termination
    if isIter:
        if cur_iter >= stopNum: return True

    # Static Evaluation Termination
    else:
        if cur_ev + one_it_an >= stopNum + 1: return True
    return False


# It decides whether the iterations will continue or not for Dynamic Termination
def dynamicTerm(isIter, bestCandList, impRate, stopNum, popSize):
    """
    Dinamik sonlandırmanın olup olmayacağına karar verir. Bool döndürür.

    Zorunlu argümanlar:
    isIter:     Sonlandırmanın iterasyon bazlı olup omadığı (bool)
    bestCandList:   Her iterasyonda sadece en iyi adayların değerlerinin saklandığı liste (list)
    impRate:        İstenen iyileşme oranı (float)
    popSize:        Popülasyon boyutu
    """
    # Eğer analiz bazlı çalışıyor ise
    if not isIter:
        stopNum = ev2it(stopNum, popSize)
    oldCand = bestCandList[-stopNum]
    newCand = bestCandList[-1]

    if oldCand * (1 - impRate) < newCand: return True
    else: return False


# Controls the population division requirement
def halfPopQ(isIter, stopNum, halfPopPercent, halfPopImpRate, popSize, bestCandList, halfPopCount):
    """
    Popülasyonu ikiye bölme iyileştirmesinin şartlarının sağlanıp sağlanmadığını kontrol eder.

    Zorunlu argümanlar:
    isIter:         Sonlandırmanın iterasyon bazlı olup omadığı (bool)
    stopNum:        Durdurma sayısı (int)
    halfPopPercent: stopNum'un hangi oranında yarıya düşürme işleminin yapılması istendiğini söyler (float)
    halfPopImpRate: Yarıya düşürülmemesini sağlamak için istenen iyileşme oranı (float)
    popSize:        Popülasyon boyutu (int)
    bestCandList:   Her iterasyonda sadece en iyi adayların değerlerinin saklandığı liste (list)
    halfPopCount:   Popülasyonu yarıya düşürme sayacı (int)
    """
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