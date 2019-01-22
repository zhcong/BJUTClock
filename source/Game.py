import Dial
from machine import Timer
import gc

timer=Timer(-1)
img_a=None
img_b=None
flag=True
level=1
max_score=52560

# show logo
def start():
    Dial.clear()
    global img_a,img_b,timer,level,max_score
    level=int((load_score()/max_score)*5) + 1 # max level is 3
    level=level if level<5 else 5 # max level is 3
    img_a=Dial.load('img/game/'+str(level)+'a.pbm',128,64)
    img_b=Dial.load('img/game/'+str(level)+'b.pbm',128,64)
    show(1) # timer can't run when it was created
    timer.init(period=500,mode=Timer.PERIODIC,callback=show)

# show img
def show(t):
    global img_a,img_b,flag,level
    img=None
    if flag:
        img=img_a
        flag=False
    else:
        img=img_b
        flag=True
    Dial.screen.blit(img, 0, 0)
    Dial.screen.text('Level',0,16)
    Dial.screen.text(str(level),16,32)
    Dial.screen.show()

# load from file
def load_score():
    f=open('level.data','r')
    l=f.read()
    f.close()
    return int(l)

def count():
    score=load_score()
    score+=1
    f=open('level.data','w')
    f.write(str(score))
    f.close()

# gc!
def stop():
    global img_a,img_b,flag
    flag=True
    img_a=None
    img_b=None
    timer.deinit()
    gc.collect()
    