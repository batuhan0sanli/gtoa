from solveTrussL import *
import copy


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


# cozum fonksiyonu sonlu elemanlar cozucuzunu 1 kez çağırır
def objectiveFunction(alan, yapi, factor, iter, iter_div):
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
    amac=w*(1+dE+sE)**(1+factor*(iter/iter_div))
    #print(amac)
    return(amac)


"""
print("--------------------------")
print("AĞIRLIK                  :",str(res[0])+"\n")
print("MESNET TEPKİLERİ         :",str(res[1][0][0])+"\n")
print("DÜĞÜM YER DEĞİŞTİRMELERİ :",str(res[1][0][1])+"\n")
print("ÇUBUK KUVVETLERİ         :",str(res[1][0][2])+"\n")
print("ÇUBUK GERİLMELERİ        :",res[1][0][3])
print("--------------------------")
"""