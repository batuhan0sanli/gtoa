# --------------- USAGE ---------------
# -------------------------------------
# Popülasyonu ikiye bölerek iterasyonlardaki analiz sayısını düşürür.

# Mod 1 = Popülasyondan seçilen adayların en iyi ilk yarısı alınır
# Mod 2 = Popülasyondan seçilen adayların %x'i en iyi aday kalanı randomdur (0 <= x <= 1)
# Mod 3 = Popülasyondan seçilen adayların %x'i en iyi, %x'i en kötü, kalanı randomdur (0 <= x <= 0.5)

# lowerLim = Popülasyon sayısı bu miktarın altına düşerse popülasyonu yarılama işlemi yapma
# -------------------------------------
# --------------- USAGE ---------------

from math import floor
from random import choices


def halfPop(pop, mod, lowerLim = 5, sel_percent = 0.2):
    # Break - Divide the population in half
    if len(pop) <= lowerLim:
        return pop

    pop.sort(key=lambda x: x[-1])
    popNum = len(pop)//2        # 5 => 3 olabilmesi için

    # Mod 1 = Popülasyondan seçilen adayların en iyi ilk yarısı alınır
    if mod == 1:
        return pop[:popNum]

    # Mod 2 = Popülasyondan seçilen adayların %x'i en iyi aday kalanı randomdur (0 <= x <= 1)
    elif mod == 2:
        selNum = floor(popNum*sel_percent)  # Seçilecek en iyi aday sayısı
        remNum = popNum - selNum            # Kalan miktar
        return (pop[:selNum] + choices(pop[selNum:], k=remNum))

    # Mod 3 = Popülasyondan seçilen adayların %x'i en iyi, %x'i en kötü, kalanı randomdur (0 <= x <= 0.5)
    elif mod == 3:
        selNum = floor(popNum*sel_percent)  # Seçilecek en iyi ve en kötü aday sayısı
        remNum = popNum - 2*selNum            # Kalan miktar
        return (pop[:selNum] + choices(pop[selNum:-selNum], k=remNum) + pop[-selNum:])