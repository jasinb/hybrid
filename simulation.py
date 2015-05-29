from websocket import create_connection
import time
import random
import json

class Agent(object):
    def __init__(self, name):
        self.name = name
        self.state = 'idle'

    def launch_computation(self, duration):
        self.state = 'computing'
        self.started = time.time()
        self.duration = duration
        self.update_state()

    def update_state(self):
        curtime = time.time()
        if self.state == 'computing':
            self.progress = float(.01 * int(100.0 * (curtime - self.started) / self.duration))
            if self.progress >= 1.0:
                self.state = 'finished'
                self.finished = curtime
        elif self.state == 'finished':
            if curtime - self.finished > 10:
                self.state = 'idle'
        elif random.random() < .05:
            # idle, launch a new computation
            self.launch_computation(random.uniform(1, 100))

    def get_state(self):
        s = { 'agent' : self.name }
        if self.state == 'computing':
            s['progress'] = self.progress
        s['state'] = self.state
        return s

ws = create_connection('wss://echo.websocket.org')

agents = []
for i in range(5):
    agents.append(Agent('Worker_{}'.format(i)))

while True:
    for a in agents:
        time.sleep(random.uniform(0.01, 0.5))
        a.update_state()
        print json.dumps(a.get_state())
    print 
    print 

    # data = 'Foobar equals hoax'
    # print 'Sending "{}"'.format(data)
    # ws.send(data)
    # result = ws.recv()
    # print 'Received "{}"'.format(result)
    # ws.close()
