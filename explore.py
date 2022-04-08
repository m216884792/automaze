import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image

import os

ppnn='100100'
imggg=1#無畫面加速探索過程
img = Image.open(f'{ppnn}/{ppnn}.png')

Img = img.convert('L')

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
    global ax
    #上下左右
    wsad=[[-1,0],[1,0],[0,-1],[0,1]]   
    #隨機行走
    t1,t2=gg
    seq=[]
    if wb[t1-1][t2]==0 or wb[t1-1][t2]==99:
        if ax!=1:
         seq.append(0)
    if wb[t1+1][t2]==0 or wb[t1-1][t2]==99:
        if ax!=0:
         seq.append(1)
    if wb[t1][t2-1]==0 or wb[t1-1][t2]==99:
        if ax!=3:
          seq.append(2)
    if wb[t1][t2+1]==0 or wb[t1-1][t2]==99:
        if ax!=2:
         seq.append(3)
    if seq!=[]:
        ax=random.choice(seq)
    return wsad[ax]


#起始位置
start1=[1,wb[0].index(0)]
print(start1)
#把入口封住以免一開始就走出去
wb[0][wb[0].index(0)]=-10




for ik in np.arange(0,5):
    a=0
    gogo=start1
    ax=4
    f = open(f'{ppnn}/test.txt', mode='a',encoding='utf-8')
    while True:
        a+=1
        r1,r2=randomwsad(gogo)
        gogo=[gogo[0]+r1,gogo[1]+r2]#更新行走位置
        if ba(gogo[0],gogo[1])==False:#走到死路
            wb[gogo[0]][gogo[1]]=1
            ax=4
        elif ba(gogo[0],gogo[1])==True:
            print('走到終點')
            ax=4
            break

        f.write(f'[{gogo[0]},{gogo[1]}] ')#儲存路徑

        if imggg==0:
            img = np.zeros((w,h,3), np.uint8)#繪製圖形
            for i1 in np.arange(0,w):
                for i2 in np.arange(0,h):
                    if wb[i1][i2]!=1:
                        img[i1][i2]=255
                    img[-2][wb[-1].index(0)]=0,0,255
                    if wb[i1][i2]==3:
                        img[i1][i2]=255,0,0
            img[gogo[0]][gogo[1]]=0,255,0
            img=cv2.resize(img, (1000,1000), interpolation=cv2.INTER_NEAREST)
            cv2.imshow('image', img)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    f.write("\n")
    f.close()
    print(f'走了{a}步')
    print(f'期望{99/a}')
    f = open(f'{ppnn}/test2.txt', mode='a',encoding='utf-8')
    f.write(f'{99/a}+')
    f.close()
