import network, Config

# create a hot-AP
def openAP(essid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=essid, password=password)

# connect to wifi
def connect(ssid,password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)

# return is online
def is_online():
    sta_if = network.WLAN(network.STA_IF)
    return sta_if.isconnected()

def connect_bjut():
    connect(Config.ssid,Config.wifi_password)

def disconnect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.disconnect()
    sta_if.active(False)

def openHibaryAP():
    openAP(Config.essid,Config.ap_password)