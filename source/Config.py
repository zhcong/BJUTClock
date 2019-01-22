# connect info
ssid='bjut_wifi'
wifi_password=''

# create AP info, not use
essid='bjut\'s clock'
ap_password=''

# time server info
time_server='wlgn.bjut.edu.cn'
time_port=8080
time_diff=81 # s
time_local=8 # utc-8

#WIFI wait time
wifi_wait_time=15

#sync pre time
sync_time=5*60*1000 # pre 10 min

#led brightness,[0,1]
brightness=0.5

#birthday
birth_month=11
birth_day=12

# save life of screen
show_start=0 # from am 0:00 to am 5:00
show_end=5

def log(s):
    f=open('log.txt','a')
    f.write(s+'\n')
    f.close()