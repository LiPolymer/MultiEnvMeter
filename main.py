from machine import Pin, I2C
import ssd1306
import dht
import machine
import time
import math
import time
from machine import ADC
from mq135 import MQ135
#Network Settings
enNet = False
netSSID = ""
netPwd = ""

mq135 = MQ135(0) #Set MQ136 AO pin to analog PIN 0

d = dht.DHT11(machine.Pin(0)) #Set DHT11 Data pin to GPIO 0
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
#display = ssd1306.SSD1306_I2C(128, 32, i2c)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
#display.text('-Realtime T&H---', 0, 0, 1)
if (enNet):
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(netSSID, netPwd)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    display.text("IP[" + str(wlan.ifconfig()).split("'")[1] + "]", 5, 40, 1)
    import webrepl
    webrepl.start()

lastdispt = "Tmp[--]"
lastdisph = "Hmd[--]"
lastdispp = "PPM[--]"
# loop
while True:
    display.text("#", 60, 0, 1)
    display.show()
    #display.text(lastdispt, 10, 20, 0)
    #display.text(lastdisph, 10, 30, 0)
    #display.text(lastdispp, 10, 40, 0)
    display.text(lastdispt, 10, 10, 0)
    display.text(lastdisph, 10, 20, 0)
    display.text(lastdispp, 10, 30, 0)
    d.measure()
    t = d.temperature()
    h = d.humidity()
    rzero = mq135.get_rzero()
    corrected_rzero = mq135.get_corrected_rzero(t, h)
    resistance = mq135.get_resistance()
    ppm = mq135.get_ppm()
    corrected_ppm = mq135.get_corrected_ppm(t, h)
    cppmstr = str(corrected_ppm)
    if(corrected_ppm < 1):
        cppmstr = "DISCONNECT"

    print("DHT11[T" + str(t) + " H" + str(h) + "]" + "MQ135[RZero: " + str(rzero) +"\t Corrected RZero: "+ str(corrected_rzero)+
          "\t Resistance: "+ str(resistance) +"\t PPM: "+str(ppm)+
          "\t Corrected PPM: "+ cppmstr +"ppm]")
    lastdispt = 'Tmp[' + str(t) + ' C]'
    lastdisph = 'Hmd[' + str(h) + ' %]'
    lastdispp = 'PPM[' + cppmstr + ']'
    #display.text(lastdispt, 10, 20, 1)
    #display.text(lastdisph, 10, 30, 1)
    #display.text(lastdispp, 10, 40, 1)
    display.text(lastdispt, 10, 10, 1)
    display.text(lastdisph, 10, 20, 1)
    display.text(lastdispp, 10, 30, 1)
    display.text("#", 60, 0, 0)
    display.show()
    time.sleep(0.5)