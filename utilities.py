import copy
import random
import sys

# --------------- UTILITIES ---------------
# -----------------------------------------

# Adds up two or more lists
def sumList(*args):
    """
    İki veya daha fazla listeyi toplamayı sağlar.

    Zorunlu argümanlar:
    args:   Birleştirilecek listeler. (lists or nested list)
    """
    if len(args) == 1: args = args[0]   # if args is a nested list: args = args[0]
    resList = [0 for i in args[0]]      # resList is a result list. Generates 0 up to the list length.
    for li in args:
        for id,element in enumerate(li):
            resList[id] += element      # Add the number to each element of resList.
    return resList


# Divides all the elements in the list by an integer
def divList(li, divNum):
    """
    Listedeki her bir elemanı bir sayıya bölmeyi sağlar.

    Zorunlu argümanlar:
    li:     Listenin kendisi (list)
    divNum: Bölünecek sayı (float or int)
    """
    return [i/divNum for i in li]


# Half List
def halfList(li):
    """
    Listeyi ortadan iki parçaya ayırarak iki liste döndürür.
    İlk eleman ilk yarısı, ikinci eleman son yarısıdır.
    Liste tek sayı ise fazlalık ikinci kısma verilir.
    LİSTE SIRALI OLMALIDIR

    Zorunlu argümanlar:
    li: Listenin kendisi (list)
    """
    num = len(li)//2
    return li[:num], li[num:]


# Means up two or more lists.
def meanList(*args):
    """
    İki veya daha fazla listenin ortalamasını alır.

    Zorunlu argümanlar:
    args:   Toplanacak listeler. (lists or nested list)
    """
    if len(args)==1: args = args[0]     # if args is a nested list: args = args[0]
    resList = [0 for i in args[0]]      # resList is a result list. Generates 0 up to the list length.

    # Sum all lists
    for i in args:
        resList = sumList(resList,i)
    return divList(resList,len(args))   # Divide the list by the total number


# Random Choice from list. But selection is not same the key cand
def randomChoice(li, cand):
    """
    Bir listeden özel bir eleman haricindeki bir başka adayın rastgele seçilmesini sağlar.

    Zorunlu argümanlar:
    li:     Seçim yapılacak liste (list)
    cand:   İstenmeyen aday (element of the list)
    """

    templi = copy.copy(li)
    templi.remove(cand)             # Removes the unwanted element
    return random.choice(templi)    # Random choice to temp list


# Clip Function
def clip(li, min, max):
    """
    Bir listedeki elemanların belirli bir aralık dışına çıktıklarında onları limite geri çekmeyi sağlar.

    Zorunlu argümanlar:
    li:     Listenin kendisi (list)
    min:    Minimum sınır değeri (float or int)
    max:    Maximum sınır değeri (float or int)
    """
    def minF(x):
        if x<min: return min
        else: return x

    def maxF(x):
        if x>max: return max
        else: return x

    return list(map(maxF, map(minF, li)))


# Fixes the length of the string
def fixLength(str, num, placeLast=True):
    """
    Yazıların düzgün görünmesi için başına veya sonuna boşluklar (" ") ekler.

    Zorunlu argümanlar:
    str:    Düzeltilmesi istenen değer (str or int or float)
    num:    str'nin olması istenen uzunluğu (int) (len(str)'den kısa olamaz.)

    Opsiyonel argümanlar:
    placeLast:  Boşluğun sona eklenmesini sağlar. (bool)
    """
    strLen = len(f"{str}")
    if strLen <= num:
        for i in range(num-strLen):
            if placeLast:
                str = f"{str}" + " "
            elif not placeLast:
                str = " " + f"{str}"
    else:
        intLen = len(f"{int(str)}")

        #Eğer 123.45 -> 4 istenmişse (123.)
        if intLen+1 == num:
            str = f"{int(str)}" + "."
        else:
            str = round(float(str),num-intLen-1)
            strLen = len(f"{str}")
            if strLen < num:
                for i in range(num - strLen):
                    if placeLast:
                        str = f"{str}" + "0"
                    elif not placeLast:
                        str = "0" + f"{str}"
    return str
# -----------------------------------------