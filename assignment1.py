from operator import itemgetter
import os

sample_plain = ['AA', 'AA', '03', '00', '00', '00', '08', '06']
sample_cipher = ['a9', '52', 'ae', '67', '3d', '92', 'd8', 'cc']

firstCipherLetter = 'AA'

S = []
statList = []
for i in range(256):
    statList.append([i,0])
j = 0


def change_to_be_hex(str):
    return int(str, base=16)

def xor_two_str(str1,str2):
    a = change_to_be_hex(str1)
    b = change_to_be_hex(str2)
    return hex(a ^ b)

def KS(index, key):
    global S,j
    S = []
    for i in range(256):
        S.append(i)
    for i in range(index):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap
        K = S[(S[i] + S[j]) % 256]
        yield K


with open('wep.out', 'rb') as f:
    hexdata = f.read().hex()

hexdata = [hexdata[i:i+2] for i in range(0, len(hexdata), 2)]
hexdata = [hexdata[i:i+7] for i in range(0,len(hexdata), 7)]

fittingMsgs = []
keySoFar = []
currentKey = []

def calculateKey(index, keySoFar):
    global currentKey, S , j
    fittingMsgs = []
    statList = []
    for i in range(256):
        statList.append([i, 0])
    for msg in hexdata:
        if msg[0] == '0' + str(2+index) and msg[1] == 'ff':
            fittingMsgs.append(msg)

    for msg in fittingMsgs:
        j = 0
        currentKey.append(int(msg[0],16))
        currentKey.append(int(msg[1],16))
        currentKey.append(int(msg[2],16))
        for key in keySoFar:
            currentKey.append(int(key))
        S = []
        KS(2+index,currentKey)
        if S[0] == int(msg[0],16) and S[1] == 0:
            XORresult = xor_two_str(firstCipherLetter,msg[3])
            XORresult = XORresult[2:]
            for m in range(256):
                if S[m] == int(XORresult,16):
                    k = (m - j - S[2+index]) % 256
                    statList[k] = [k,statList[k][1]+1]
        currentKey = []


    temp = sorted(statList, key=itemgetter(1), reverse=True)
    keySoFar.append(temp[0][0])
    if len(keySoFar) != 5:
        calculateKey(index+1, keySoFar)

trueKey = [77,235,120,38,161]


calculateKey(1,keySoFar)
print('[{}]'.format(', '.join(hex(x)[2:] for x in keySoFar)))

os.system("pause")

'''
KS(256,trueKey)
keystream = PRGA(S)

keystreamList = []
for key in keystream:
    if len(keystreamList) != len(sample_cipher):
        keystreamList.append(hex(key))
    else:
        break


output = []
for c in sample_cipher:
    i = 0
    key = keystreamList[i]
    xor = xor_two_str(c, key[2:])
    i += 1
    output.append(xor[2:])

print(sample_plain)
print(output)
'''


