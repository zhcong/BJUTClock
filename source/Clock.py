from machine import RTC
import time
import Dial, BJUTTime, WIFI, Config, Game
import gc

def init(r):
    global rtc,hours,minute
    rtc=r
    _date_time=rtc.datetime()
    hours=_date_time[4] if _date_time[4]<=12 else _date_time[4]-12
    minute=_date_time[5]

# check time change
def show_clock():
    global hours,minute,rtc
    times=rtc.datetime()
    Dial.show(time_str(times),'am' if times[4]<=12 else 'pm',times[3]+1,times[2])
    hours=times[4] if times[4]<=12 else times[4]-12
    minute=times[5]

# check time change
def check_clock(t):
    global hours,minute,rtc
    times=rtc.datetime()
    if not (hours==times[4] or hours==times[4]-12) or not (minute==times[5]):
        show_clock()
        if minute==0 or minute==30:
            Dial.flash()

# convert to time string
def time_str(times):
    return "%02d:%02d"%(times[4] if times[4]<=12 else times[4]-12,times[5])

# set time by sync
def sync_clock(t):
    try:
        Dial.is_sync=True
        Dial.is_sync_error=False
        show_clock()

        # check birthday
        times=rtc.datetime()
        if times[1]==Config.birth_month and times[2]==Config.birth_day:
            Dial.is_love=True
        else:
            Dial.is_love=False

        # save life of screen
        t=time.localtime()
        if t[3]>=Config.show_start and t[3]<=Config.show_end:
            Dial.off()
            return
        else:
            Dial.on()

        WIFI.connect_bjut()

        count=0
        while not WIFI.is_online():
            count+=1
            if count==Config.wifi_wait_time: 
                Dial.is_sync=False
                Dial.is_sync_error=True
                show_clock()
                return
            time.sleep(1)
        Config.log('start sync at %d:%d:%d'%(time.localtime()[3],time.localtime()[4],time.localtime()[5]))
        t,start_t=BJUTTime.get_time()
        Config.log('local time is %d:%d:%d'%(time.localtime()[3],time.localtime()[4],time.localtime()[5]))
        set_time(t,start_t)
        Config.log('new time is %d:%d:%d'%(time.localtime()[3],time.localtime()[4],time.localtime()[5]))
        
        WIFI.disconnect()
        Dial.is_sync=False
        show_clock()

        # update game score
        Game.count()
        gc.collect()
    except Exception as e:
        print(e)

# set time use Timestamp
def set_time(timestamp,start_t):
    global rtc
    diff=int(time.time()-start_t)
    t=time.localtime(timestamp+diff)
    rtc.datetime((t[0],t[1],t[2],t[6],t[3],t[4],t[5],0)) # weak 0-6

