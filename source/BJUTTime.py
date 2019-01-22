import socket, time, Config

# synchronize time by http head(not https's ServerHello),
# this is Beijing University of Technology's server
# after comparison, this server is 106(+106) seconds faster.(2018-12-28)
# and convert GMT's time to china's time

time_diff=Config.time_diff

mouth_dict={
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12
}
week_dict={
    'Mon':1,
    'Tue':2,
    'Wed':3,
    'Thu':4,
    'Fri':5,
    'Sat':6,
    'Sun':7
}
def get_time():
    try:
        global port,server,time_diff
        server=socket.getaddrinfo(Config.time_server,Config.time_port)[0][-1]
        s = socket.socket()
        s.connect(server)
        s.send("HEAD / HTTP/1.1\r\nHost: wlgn.bjut.edu.cn\r\n\r\n")
        start_t=time.time()
        data=s.recv(2048)
        s.close()
        time_GMT=data.decode().split('\r\n')[2].split(' ')
        year=int(time_GMT[4])
        mouth=time_GMT[3]
        week=time_GMT[1].replace(',','')
        day=int(time_GMT[2])
        hour=int(time_GMT[5].split(':')[0])
        minute=int(time_GMT[5].split(':')[1])
        second=int(time_GMT[5].split(':')[2])
        t=time.mktime((year,mouth_dict[mouth],day,hour,minute,second,week_dict[week],1,0)) # this week has error
        t=t+8*60*60-time_diff
        return t,start_t
    except Exception as e:
        print(e)
        return 0