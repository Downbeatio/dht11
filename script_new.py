from subprocess import check_output
from subprocess import call
import time
import plotly
from plotly.offline import plot
#import plotly.plotly as py
from plotly.graph_objs import *

a = []
b = []

def fan_init():
	init = call('echo 17 > /sys/class/gpio/export', shell=True)
	direction = call('echo out > /sys/class/gpio/gpio17/direction', shell=True)
	init
	direction
        time.sleep(3)
	fan_off()
	
def fan_on():
	fan_on = call('echo 0 > /sys/class/gpio/gpio17/value', shell=True)
	fan_on
	
def fan_off():
	fan_off = call('echo 1 > /sys/class/gpio/gpio17/value', shell=True)
	fan_off
	
	
fan_init()

while True:
        out = check_output(["./dht"])
        if out != ("Data not good, skip\n"):
                out = out.split(" ")
                humd = float(out[0])
                temp = float(out[1])
                a.append(humd)
                b.append(temp)
                if len(a) == 900: #900: 15 minutes
                        trace0 = Scatter(
                                x=range(len(a)),
                                y=a,
                        	name = 'humidity'
			)
                        trace1 = Scatter(
                                x=range(len(a)),
                                y=b,
				name = 'temp'
                        )
                        data = Data([trace0, trace1])
#                        py.plot(data, filename = 'basic-line')
                        plot(data, filename='/var/www/html/graph1.html')
                        a = []
                        b = []
		if  humd > 62:
			fan_on()
		else:
			fan_off()
			
        time.sleep(1)


