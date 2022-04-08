import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image

import os
import re
ppnn='100100'
img = Image.open(f'{ppnn}/{ppnn}.png')

Img = img.convert('L')
imggg=0
threshold = 240
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
#圖片二值化
photo = Img.point(table, '1')
photo.save(f"{ppnn}/{ppnn}dark.png")
img=cv2.imread(f'{ppnn}/{ppnn}dark.png')
t,rst=cv2.threshold(img,58,255,cv2.THRESH_BINARY)
cv2.imwrite(f'{ppnn}/{ppnn}dark.png',rst)

img=cv2.imread(f'{ppnn}/{ppnn}dark.png')
print(img.shape)
w,h,rgb=img.shape
print(w)
wb=[]
for h1 in np.arange(0,h):
    h2=[]
    for w1 in np.arange(0,w):
        if (img[h1][w1]==[0,0,0]).all():
            h2.append(1)
        else:
            h2.append(0)
    wb.append(h2)

wb[-2][wb[-1].index(0)]

#定義規則
import random

#終止
def ba(i1,i2):
    try:
        if (wb[i1-1][i2]+wb[i1+1][i2]+wb[i1][i2+1]+wb[i1][i2-1])==3:
            return False
    except:
        return True

def randomwsad(gg):
    #上下左右
    wsad=[[-1,0],[1,0],[0,-1],[0,1]]   
    #隨機行走
    t1,t2=gg
    seq=[]
    if wb[t1-1][t2]==0 or wb[t1-1][t2]==99:
        seq.append(0)
    if wb[t1+1][t2]==0 or wb[t1-1][t2]==99:
        seq.append(1)
    if wb[t1][t2-1]==0 or wb[t1-1][t2]==99:
        seq.append(2)
    if wb[t1][t2+1]==0 or wb[t1-1][t2]==99:
        seq.append(3)
    return wsad[random.choice(seq)]

#起始位置
start1=[1,wb[0].index(0)]
print(f'起點{start1}')
#把入口封住以免一開始就走出去
wb[0][wb[0].index(0)]=-10


while True:
    a=0
    gogo=start1

    img = np.zeros((w,h,3), np.uint8)
    for i1 in np.arange(0,w):
        for i2 in np.arange(0,h):
            if wb[i1][i2]!=1:
                img[i1][i2]=255
            img[-2][wb[-1].index(0)]=0,0,255
            if wb[i1][i2]==3:
                img[i1][i2]=255,0,0

    with open(f'{ppnn}/test2.txt',encoding='utf-8') as f:
        data = f.readlines()
    output=data[0].split('+')
    del output[-1]
    axr=output.index(max(output))

    with open(f'{ppnn}/test.txt',encoding='utf-8') as f:
        data = f.readlines()
    output=data[axr].split(' ')
    del output[-1]#路徑

    f = open(f'{ppnn}/test.txt', mode='a',encoding='utf-8')
    while True:
        a+=1
        xc=False
        ann=[]

        gogo=[gogo[0],gogo[1]]

        af=1
        apx=[]
        for ix in output:
            if ix==f'[{gogo[0]},{gogo[1]}]':
                if af!=len(output):
                    apx.append(output[af])
            af+=1
        if len(apx)!=0:
            gg=apx[-1]
            gg=re.search(r'\d*,\d*',gg).group(0)
            gg=gg.split(',')
            gogo=[int(gg[0]),int(gg[-1])]#更新行走位置

        
        else:
            r1,r2=randomwsad([gogo[0],gogo[-1]])
            gogo=[gogo[0]+r1,gogo[-1]+r2]#更新行走位置

        if ba(gogo[0],gogo[1])==False:#走到死路
            wb[gogo[0]][gogo[1]]=3
        if [gogo[0],gogo[1]]==[w-2,wb[-1].index(0)]:
            print('走到終點')
            break
        f.write(f'[{gogo[0]},{gogo[1]}] ')
        
        
        
        if imggg==0:
            img[gogo[0]][gogo[1]]=0,255,0
            img2=cv2.resize(img, (1000,1000), interpolation=cv2.INTER_NEAREST)
            cv2.imshow('image', img2)
            if cv2.waitKey(1) & 0xFF == 27:
                break
    f.write("\n")
    f.close()
    print(f'走了{a-1}步')
    print(f'期望{99/a}')
    print('x'*50)
    f = open(f'{ppnn}/test2.txt', mode='a',encoding='utf-8')
    f.write(f'{99/a}+')
    f.close()

