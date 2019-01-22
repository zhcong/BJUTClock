# -*- coding: UTF-8 -*-
import Screen, Dial, Clock, Config, LED, Game
from machine import Pin,SPI,Timer,RTC
import time, gc

# change mode
def change_mode(pin):
    if pin.value()==0:
        if Dial.mode=='game':
            Dial.mode='clock'
            Game.stop()
            Clock.show_clock()
    else:
        if Dial.mode=='clock':
            Dial.mode='game'
            Game.start()

# led init
led=Pin(13,Pin.OUT)
led.value(0)

# miso=Pin(16) is empty
spi=SPI(sck=Pin(2),mosi=Pin(0),miso=Pin(16),baudrate=2400000)
s=Screen.create(128, 64, spi, dc=Pin(5), res=Pin(4))

Dial.init(s,led)
Dial.show_logo()
time.sleep(1)
Dial.clear()

Clock.init(RTC())
Clock.sync_clock(1)

timer = Timer(0)
timer.init(period=1000,mode=Timer.PERIODIC,callback=Clock.check_clock)

timer2 = Timer(1)
timer2.init(period=Config.sync_time,mode=Timer.PERIODIC,callback=Clock.sync_clock)

button=Pin(15,Pin.IN)
button.irq(handler=change_mode,trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)