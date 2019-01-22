import framebuf, math, time
import LED, Config
from machine import Timer

screen = None
led=None
is_sync=False
is_sync_error=False
is_love=False
mode='clock' # clock or game

# load pbm file
def load(file,width,height):
    f=open(file, 'r')
    f.readline()
    f.readline()
    f.readline()
    data = bytearray(f.read())
    f.close()
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)

# show logo
def show_logo():
    global screen
    fbuf=load('img/logo.pbm',64,64)
    screen.invert(1)
    screen.blit(fbuf, 32, 0)
    screen.show()

# icos class
ico = {
    '0':None,
    '1':None,
    '2':None,
    '3':None,
    '4':None,
    '5':None,
    '6':None,
    '7':None,
    '8':None,
    '9':None,
    'am':None,
    'pm':None,
    'flash':None,
    'cycle':None
}
# load all ico file
def init(s,l):
    global screen,led
    screen=s
    led=LED.create(l)
    ico['0']=load('img/0.pbm',25,64)
    ico['1']=load('img/1.pbm',25,64)
    ico['2']=load('img/2.pbm',25,64)
    ico['3']=load('img/3.pbm',25,64)
    ico['4']=load('img/4.pbm',25,64)
    ico['5']=load('img/5.pbm',25,64)
    ico['6']=load('img/6.pbm',25,64)
    ico['7']=load('img/7.pbm',25,64)
    ico['8']=load('img/8.pbm',25,64)
    ico['9']=load('img/9.pbm',25,64)
    ico['flash']=load('img/flash.pbm',3,64)
    ico['am']=load('img/am.pbm',25,32)
    ico['pm']=load('img/pm.pbm',25,32)
    ico['cycle']=load('img/cycle.pbm',25,32)
    ico['cycle_error']=load('img/cycle_error.pbm',25,32)
    ico['love']=load('img/love.pbm',25,32)

week_dict={
    1:'Mo',
    2:'Tu',
    3:'We',
    4:'Th',
    5:'Fr',
    6:'Sa',
    7:'Su'
}

# show clock
def show(time_str='09:19',part='am',week=1,day=1):
    global is_sync,is_sync_error,mode
    if mode=='game':
        return
    try:
        t1=time_str[0]
        t2=time_str[1]
        t3=time_str[3]
        t4=time_str[4]

        screen.fill(0)
        if part=='am':
            screen.blit(ico['am'], 0, 0)
        elif part=='pm':
            screen.blit(ico['pm'], 0, 0)
        if is_sync:
            screen.blit(ico['cycle'], 0, 32)
        elif is_sync_error:
            screen.blit(ico['cycle_error'], 0, 32)
        elif is_love:
            screen.blit(ico['love'], 0, 32)
        else:
            screen.text(week_dict[week], 4, 32)
            screen.text("%02d"%day, 4, 46)
        screen.blit(ico[t1], 25, 0)
        screen.blit(ico[t2], 50, 0)
        screen.blit(ico['flash'], 75, 0)
        screen.blit(ico[t3], 78, 0)
        screen.blit(ico[t4], 103, 0)
    except Exception as e:
        print(e)

    screen.show()

# clear dial
def clear():
    screen.invert(0)
    screen.fill(0)
    screen.show()

# led flash
def led_flash(t):
    global led
    for _ in range (10):
        for i in range(314):
            led.brightness(math.sin(i/100)*Config.brightness)
            time.sleep_ms(10)
    led.off()

# led flash with timer
def flash():
    timer = Timer(-1)
    timer.init(period=10,mode=Timer.ONE_SHOT,callback=led_flash)

def on():
    screen.poweron()

def off():
    screen.poweroff()