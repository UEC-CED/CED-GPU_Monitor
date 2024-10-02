# ----------------------------------------------------------------------
# CED GPUServer.
# ----------------------------------------------------------------------
import os
import time
import threading
import re
from enum import Enum
import paramiko
import csv

# dummy observer.
def on_change(host, status=None): pass

class Status(Enum):
    UNKNOWN = 0
    BAD = 1
    STUCK = 2
    REFUSED = 3
    GOOD = 4
        
class CEDHost:
    USER_NAME ="cadmin"
    KEY_FILEPATH = "/home/cadmin/.ssh/id_rsa_gpu"

    SSHOPTIONS = f'\
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -i {KEY_FILEPATH}  \
    '
    PINGWAIT = 3
    WHOCMD = "w"
    MEMCMD = "free -h"

    UPDATER_WAIT = 6            # iXX
    WATCHER_WAIT = 10            # XXX
    WATCHER_TOLERANCE = 5       # XXX

    GET_GPUSTATUS_CMD = "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv"

    
    def __init__(self, color, id, observer=on_change):
        self.id = id
        self.observer = observer
        self.username = CEDHost.USER_NAME
        self.name = f'{color}{id:02d}'
        self.fqdn = self.name + ".ced.cei.uec.ac.jp"
        self.whocmd = f"ssh {CEDHost.SSHOPTIONS} -q {self.fqdn} {CEDHost.WHOCMD}"
        self.memcmd = f"ssh {CEDHost.SSHOPTIONS} -q {self.fqdn} {CEDHost.MEMCMD}"
        self.status = Status.UNKNOWN
        self.n_users = (0, 0)
        self.load = None
        self.mem = None
        self.gpustatus = None
        self.watcher = threading.Thread(target=self.watch, name=self.name+'-watcher')
        self.updater = threading.Thread(target=self.update, name=self.name+'-updater')
        self.updated = False
        self.wdt = 0

    def start(self):
        self.watcher.start()
        self.updater.start()

    def pingable(self):
        r = False
        with os.popen(f'ping -w {CEDHost.PINGWAIT} {self.fqdn}') as f:
            for line in f:
                pass
            if not f.close(): r = True
        return r

    def logging_gpu(self, port):
        rsa_key = paramiko.RSAKey.from_private_key_file(CEDHost.KEY_FILEPATH)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(self.fqdn, port, self.username, pkey=rsa_key)
            command = CEDHost.GET_GPUSTATUS_CMD
            stdin,stdout,stderr = client.exec_command(command)
            output = stdout.read().decode("utf-8")
            
            return output
        finally:
            client.close()


    def restart_updater(self):
        self.updater = threading.Thread(target=self.update, name=self.name+'-updater')
        self.updater.start()
    
    def update(self):
        while True:
            self.wdt = 0

            if not self.pingable(): self.status = Status.BAD

            if self.status != Status.BAD:
                users = []
                lapat = 'load average: (.*)$'
                load = None
                with os.popen(self.whocmd) as f:
                    for lineno, line in enumerate(f):
                        if lineno == 0:
                            if m := re.search(lapat, line):
                                load = m.group(1)
                        elif lineno > 1:
                            users.append(line.split(' ')[0])

                    self.status = Status.STUCK if f.close() else Status.GOOD

                if self.status == Status.GOOD:
                    self.n_users = (len(users), len(set(users)))
                    self.load = load
                    with os.popen(self.memcmd) as f:
                        for line in f:
                            if line.startswith('Mem:'):
                                self.mem = line.split()[-1]
                                break
                    #get status of gpus
                    self.gpustatus = self.logging_gpu(22)     

            self.updated = True
                    
            time.sleep(CEDHost.UPDATER_WAIT)
            
    def watch(self):
        self.wdt= 0
        while True:
            if self.updated:
                self.observer(self, self.status)
                self.updated = False
            if self.wdt >= CEDHost.WATCHER_TOLERANCE:
                self.observer(self, Status.STUCK)
                self.restart_updater()

            time.sleep(CEDHost.WATCHER_WAIT)
            self.wdt += 1
