# genellik
# kesinlik
# sağlamlık
# verimlilik


# Gerekli kütüphaneler import ediliyor
# ------------------------------------
from solveTrussL import *
import copy
# ------------------------------------



# OpenSees kütüphanesini kullanarak 2 ve 3 boyutlu kafes sistemleri çözer.
# -------------------------------------------------------------------------------
# Girdi biçimi aşağıdaki yığılmış liste şeklindedir.
# [
#     [malzemenin elastisite modülü, birim ağırlığı],
#     [[düğüm numarası, x koordinatı, y, varsa z], ...],
#     [[mesnetin düğüm numarası, x yönü tutulu mu? (1 veya 0), y, varsa z], ...],
#     [1 numaralı kesitin alanı, 2 numaralı kesitin alanı, ...],
#     [[çubuk numarası, kesit numarası, başlangıç düğümü, bitiş düğümü], ...]
#     [
#         1 numaralı yükleme durumu
#         [[düğüm numarası, x yönündeki kuvvet, y, varsa z], ...],
#         2 numaralı yükleme durumu
#         [[düğüm numarası, x yönündeki kuvvet, y, varsa z], ...],
#         ...
#     ]    
# ]
# -------------------------------------------------------------------------------
# [w, [[r1,u1,n1,s1], [r2,u2,n2,s2], ...]] biçiminde çıktı verir.
#     w  : yapı ağırlığı
#     r1 : 1 numaralı yükleme için mesnet reaksiyonları
#     u1 : 1 numaralı yükleme için düğüm yer değiştirmeleri
#     n1 : 1 numaralı yükleme için çubuk kuvvetleri
#     s1 : 1 numaralı yükleme için çubuk gerilmeleri
#     r2 : 2 numaralı yükleme için mesnet reaksiyonları
#     u2 : ...
# -------------------------------------------------------------------------------



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

# cozum fonksiyonu sonlu elemanlar cozucuzunu 1 kez çağırır
def objectiveFunction(alan,yapi):
    yeniYapi=copy.deepcopy(yapi)
    yeniYapi[3]=alan
    sol=solveTrussL(yeniYapi)
    w=sol[0]
    dR=[abs(i)/2 for i in sol[1][0][1]]
    sR=[abs(i)/25 for i in sol[1][0][3]]
    # kapasite aşımı
    # Aşan kısmın ceza olaran düşünülmesi daha uygun olur.

    dE=sum([i-1 for i in dR if i>1])
    sE=sum([i-1 for i in sR if i>1])
    amac=w*(1+dE+sE)**2
    #print(amac)
    return(amac)


# toplam yer değiştirme ihlali: 6.37 (1.445, 2.38, 2.36)
# toplam gerilme ihlali: 30.37 (1.4, 1.81)
# Bunu optimize et: W = w(1+p)^2
# W = 5968.63*(1+6.37+30.37)^2=8.5*10^6 KÖTÜ
# W = 5968.63*(1+1.445+2.38+2.35+1.4+1.81)^2 İYİ
# pipeline

denemeAlan=[22.12, 10.21, 4.55, 1.23, 5.66, 34.33, 23.11, 24.33, 11.34, 3.23]

"""
print("--------------------------")
print("AĞIRLIK                  :",str(res[0])+"\n")
print("MESNET TEPKİLERİ         :",str(res[1][0][0])+"\n")
print("DÜĞÜM YER DEĞİŞTİRMELERİ :",str(res[1][0][1])+"\n")
print("ÇUBUK KUVVETLERİ         :",str(res[1][0][2])+"\n")
print("ÇUBUK GERİLMELERİ        :",res[1][0][3])
print("--------------------------")
"""