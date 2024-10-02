# CED monitor(especially for orange*).

from flask import Flask, render_template
from ced import *
import time

def now():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

SNO, ENO = 1, 4                 # start and end number of machines.

host_status = [(
    "???",                      # hostname.
    "???",                      # status.
    "???",                      # number of users.
    "???",                      # load average.
    "???",                      # current time.
    "#ffffff"                   # color for load average column.
    "???"                       # available memory.
) for _ in range(SNO, ENO+1)]

gpu_status = [(
    "???",          #hostname
    ["???"],        #index
    ["???"],        #gpuname
    ["???"],        #utilization of gpu(%)
    ["???"],        #used memory(MiB)
    ["???"]         #total memory(MiB)  
) for _ in range(SNO, ENO+1)]

def load_to_color(load):
    LX, UX, LY, UY = 0.0, 10.0, 255, 0 # XXX.
    if load < LX:
        intensity = 255
    else:
        a = (UY-LY)/(UX-LX)
        b = LY-a*LX
        intensity = int((load-LX)*a+b)
        intensity = max(min(intensity, 255), 0)
    return f'#ff{intensity:02x}{intensity:02x}'

def on_status_change(host, status):
    load = host.load
    if not load:
        n_users = "-"
        load = "-"
        load_color = "#ffffff"
        available_memory = "-"
    else:
        # #users.
        n_users = str(host.n_users[0])
        if host.n_users[0] != host.n_users[1]:
            n_users += f'({host.n_users[1]})'
        # load color.
        load_color = load_to_color(float(load.split(',')[0]))
        available_memory = host.mem + "B"
        
    host_status[host.id-SNO] = (host.name, 
                                status.name, 
                                n_users,
                                load,
                                now(),
                                load_color,
                                available_memory)
    
    log = host.gpulog
    gpu_status[host.id-SNO] = (host.name,
                               [row[1] for row in log],
                               [row[2] for row in log],
                               [row[3] for row in log],
                               [row[4] for row in log],
                               [row[5] for row in log]
                               )

hosts = [CEDHost("gpu", i, on_status_change) for i in range(SNO, ENO+1)]

# # brown01.
# hosts += [CEDHost("brown", 1, on_status_change)]

# # gpu01-04.
# for i in range(1, 4+1):
#     hosts += [CEDHost("gpu", i, on_status_change)]

for host in hosts:
    host.start()

app = Flask(__name__)

@app.route('/')
def monitor():
    return render_template('monitor.html', 
                           host_status=host_status,
                           gpu_status=gpu_status, 
                           localtime=now())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=23456) # XXX

