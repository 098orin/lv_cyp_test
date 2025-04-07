
def lock(key: int,IV: int,data: int,b=0) -> int:
    if len(str(key)) < 11:
        return lock(str(key) + "0",IV,data,b)
    if b != 5:
        return lock(base(key,5),IV,base(data,5),5)
    Answer = ""
    sBox = s_box(data,key)
    i = j = 0
    for k in range(len(data)):
        i = (i+1) % len(sBox)
        j = (j + sBox[i]) % len(sBox)
        if str(data[k]) == str(sBox[j]):
            Answer = Answer + "0"
        else:
            Answer = Answer + str(int(data[k]) + int(sBox[j]))
    i = ""
    k = 0
    for j in list(Answer):
        k += 1
        if k == 1:
            i = 1 + int(j)
        else:
            i = str(i) + str(j)
    Answer = int(i)
    Answer = Answer * IV + IV
    sBox = s_box(Answer, str(IV)+str(key), IV=True)
    Answer = "1"
    for i in sBox:
        Answer = Answer + str(i)
    return Answer

def unlock(key: int,IV: int, data: int,b=0) -> int:
    if len(str(key)) < 11:
        return unlock(str(key) + "0",IV,data,b)
    if b != 5:
        sBox = s_box(data[1:],str(IV)+base(key,5),IV=True,unlock=True)
        Answer = str("".join(map(str,sBox)))
        Answer = int(Answer) - int(str(IV) + str(base(key,5)))
        Answer = str((Answer - IV) // IV)
        k = 0
        i = ""
        for k in range(len(Answer)):
            if k == 0:
                i = int(Answer[0]) - 1
            else:
                i = str(i) + Answer[k]
        return unlock(base(key,5),IV,i,5)
    sBox = s_box(data,key)
    i = j = k = 0
    Answer = ""
    data = str(data)
    for k in range(len(data)):
        i = (i+1) % len(sBox)
        j = (j + int(sBox[i])) % len(sBox)
        if "0" == str(sBox[j]):
            Answer = Answer + str(sBox[j])
        else:
            Answer = Answer + str(int(data[k]) - int(sBox[j]))
    return str(int(Answer,5))

def s_box(data,key,IV=False,unlock=False):
    sBox = list() 
    if unlock:
        for i in data:
            sBox.append(i)
    elif IV:
        for i in str(int(data)+int(key)):
            sBox.append(i)
    else:
        for i in range(len(str(data))):
            sBox.append(i%6)

    data = str(data)
    key = str(key)
    if unlock:
        for i in range(len(sBox)):
            i2 = len(sBox) - i -1
            j = (i2 + int(key[i2%len(key)])) %len(sBox)
            sBox[i2], sBox[j] = sBox[j], sBox[i2]
    else:
        for i in range(len(sBox)):
            j = (i + int(key[i % len(key)])) % len(sBox)
            sBox[i], sBox[j] = sBox[j], sBox[i]

    return sBox
        

def base(num: int, base: int) -> int:
    num = int(num)
    if num == 0:
        return "0"
    
    digits = ""
    while num > 0:
        remainder = num % base
        if remainder < 10:
            digits = str(remainder) + digits  # 0-9の場合
        else:
            digits = chr(remainder - 10 + ord('A')) + digits  # 10-15の場合（16進数用）
        num //= base

    return digits
