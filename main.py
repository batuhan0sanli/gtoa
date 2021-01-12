# FOR MULTIPLE ANALYSIS

import GTOA
from tqdm.auto import trange
from utilities import fixLength

"""
Group Teaching Optimization Algorithm (GTOA) için çoklu çalıştırılabilen dosyadır.
Tüm argümanlar opsiyoneldir. Argüman girilmez ise gerekli argümanlar user.py dosyasından çekilecektir.

Popülasyon Bilgisi:
popSize:        Popülasyon boyutu (int)
stopCriteria:   Durdurma kriteri (str)
stopNum:        Durdurma sayısı (int)
impRate:        İstenen iyileşme oranı (float)
F:              Öğrenme katsayısı / F değeri (int)
inputSize:      Tasarım değişkeni sayısı (int)
minLimit:       İstenen minimum değer (int or float)
maxLimit:       İstenen maximum değer (int or float)
limitless:      Adayın alabileceği değerlerin sınırsız olduğunu söyler (bool)

İyileştirme Ayarları:
adaptive_pen:       Adaptif ceza iyileştirmesinin aktif olma durumu (bool)
half_population:    Popülasyonu yarıya düşürme iyileşmesinin aktif olma durumu (bool)
halfPopImpRate:     Yarıya düşürülmemesini sağlamak için istenen iyileşme oranı (float)
halfPopPercent:     stopNum'un hangi oranında yarıya düşürme işleminin yapılması istendiğini söyler (float)
mod:                Popülasyonu yarıya düşürme iyileştirmesinde tercih edilen mod [1, 2, 3]
lowerLim:           Popülasyon boyutunun lowerLim değerinin altına düştüğünde düşürme işleminin yapılmaması (int)
sel_percent:        Mod 2 ve 3 için tercih edilen seçim oranı (float)

Yazdırma Ayarları:
printSpace:     Aralarda boşluk bırakır (bool)
printIteration: İterasyon hakkında bilgileri yazdırır -iterasyon no, analiz no, popülasyon boyutu, en iyi çözüm- (bool)
printBestCand:  En iyi adayı yazdırır (bool)

CSV Kayıt Ayarları:
saveCSV:    CSV kaydının yapılmasını sağlar (bool)
onlyBest:   Tüm popülasyonun değil sadece en iyi adayın kaydedilmesini sağlar (bool)
csvMode:    CSV kaydında tercih edilecek kayıt modu [self.csvMode, 'w' ..]
"""

# --------------- TESTS ---------------
# -------------------------------------
class Test():
    def __init__(self, numRun = 25, popSize=50, saveCSV=True, onlyBest=True, csvMode='a'):
        self.numRun = numRun
        self.popSize = popSize
        self.csvMode = csvMode
        self.onlyBest = onlyBest
        self.saveCSV = saveCSV

    def standart(self):
        """
        user.py'de girilen ayarlar ile birden çok analiz yaptırır.
        """
        for i in trange(self.numRun, leave=False):
            GTOA.GTOA(saveCSV=self.saveCSV, onlyBest=self.onlyBest, csvMode=self.csvMode)
        return None

    def popBoyut(self, popSizes:list):
        """
        Farklı popülasyon boyutlarıyla testler yapar
        popSizes = Denenmek istenen popülasyon büyüklükleri (list)
        """
        self.popSizes = popSizes
        for i, pSize in zip(trange(len(self.popSizes), desc="Total Run     "), self.popSizes):
            for j in trange(self.numRun, desc=f'N={fixLength(pSize, 4)}        ', leave=False):
                GTOA.GTOA(popSize=pSize, saveCSV=self.saveCSV, onlyBest=self.onlyBest, csvMode=self.csvMode)
        return None

    def fDeger(self):
        """
        Farklı F değerleriyle [1, 2] testler yapar
        """
        self.F = [1, 2]
        for i, Fi in zip(trange(len(self.F), desc="Total Run     "), self.F):
            for j in trange(self.numRun, desc=f'F={fixLength(Fi, 4)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, F=Fi, saveCSV=self.saveCSV, onlyBest=self.onlyBest, csvMode=self.csvMode)
        return None

    def iyilesme(self, FF0=False, TF0=False, FT1=False, FT2=False, FT3=False, TT1=False, TT2=False, TT3=False):
        """
        İyileşme fonksiyonlarının etkisinin testini yapar

        FF0:    Adaptive Penalty Kapalı | Popülasyon Düşürme Kapalı (bool)
        TF0:    Adaptive Penalty Açık   | Popülasyon Düşürme Kapalı (bool)
        FT1:    Adaptive Penalty Kapalı | Popülasyon Düşürme Açık | Mod 1 (bool)
        FT2:    Adaptive Penalty Kapalı | Popülasyon Düşürme Açık | Mod 2 (bool)
        FT3:    Adaptive Penalty Kapalı | Popülasyon Düşürme Açık | Mod 3 (bool)
        TT1:    Adaptive Penalty Açık   | Popülasyon Düşürme Açık | Mod 1 (bool)
        TT2:    Adaptive Penalty Açık   | Popülasyon Düşürme Açık | Mod 2 (bool)
        TT3:    Adaptive Penalty Açık   | Popülasyon Düşürme Açık | Mod 3 (bool)
        """
        self.FF0 = FF0
        self.TF0 = TF0
        self.FT1 = FT1
        self.FT2 = FT2
        self.FT3 = FT3
        self.TT1 = TT1
        self.TT2 = TT2
        self.TT3 = TT3

        # Adaptive Penalty Kapalı | Popülasyon Düşürme Kapalı
        if FF0:
            for j in trange(self.numRun, desc=f'N={fixLength("F F -", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=False, half_population=False, mod=1, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Açık | Popülasyon Düşürme Kapalı
        if TF0:
            for j in trange(self.numRun, desc=f'N={fixLength("T F -", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=True, half_population=False, mod=1, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Kapalı | Popülasyon Düşürme Açık | Mod 1
        if FT1:
            for j in trange(self.numRun, desc=f'N={fixLength("F T 1", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=False, half_population=True, mod=1, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Kapalı | Popülasyon Düşürme Açık | Mod 2
        if FT2:
            for j in trange(self.numRun, desc=f'N={fixLength("F T 2", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=False, half_population=True, mod=2, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Kapalı | Popülasyon Düşürme Açık | Mod 3
        if FT3:
            for j in trange(self.numRun, desc=f'N={fixLength("F T 3", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=False, half_population=True, mod=3, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Açık | Popülasyon Düşürme Açık | Mod 1
        if TT1:
            for j in trange(self.numRun, desc=f'N={fixLength("F T 1", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=True, half_population=True, mod=1, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Açık | Popülasyon Düşürme Açık | Mod 2
        if TT2:
            for j in trange(self.numRun, desc=f'N={fixLength("F T 2", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=True, half_population=True, mod=2, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)

        # Adaptive Penalty Açık | Popülasyon Düşürme Açık | Mod 3
        if TT3:
            for j in trange(self.numRun, desc=f'N={fixLength("F T 3", 5)}        ', leave=False):
                GTOA.GTOA(popSize=self.popSize, adaptive_pen=True, half_population=True, mod=3, saveCSV=self.saveCSV, onlyBest=self.onlyBest,
                          csvMode=self.csvMode)
        return None
# -------------------------------------
# --------------- TESTS ---------------


# --------------- KULLANIMI ---------------
# -----------------------------------------
# Test().standart():    user.py'de girilen ayarlar ile birden fazla kez analiz yaptırır
# Test().popBoyut():    Farklı popülasyon boyutlarıyla testler yapar
# Test().fDeger():      Farklı F değerleriyle testler yapar
# Test().iyilesme():    İyileşme fonksiyonlarının etkisinin testini yapar
# -----------------------------------------


if __name__ == '__main__':
    print("'result/' klasörünün varlığını ve içeriğini kontrol ediniz!")
    Test(numRun=30).popBoyut(popSizes=[10, 20, 30, 40, 50, 100, 200, 500, 1000])