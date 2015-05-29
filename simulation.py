from websocket import create_connection
import time
import random
import json

class Channel(object):
    def __init__(self, conn):
        self.ws = create_connection(conn)
        self.ref = 0

    def _makeref(self):
        self.ref = self.ref + 1
        return self.ref

    def join(self, chan):
        d = json.dumps({
            'event': 'phx_join',
            'topic': chan,
            'ref': self._makeref(),
            'payload': {}
            })
        self.ws.send(d)
        self.chan = chan
        print self.ws.recv()


    def send(self, event, payload):
        d = json.dumps({
            'topic': self.chan,
            'event': event,
            'payload': payload,
            'ref': self._makeref()
            })
        self.ws.send(d)
        # print self.ws.recv()

class Agent(object):
    def __init__(self, name):
        self.name = name
        self.state = 'idle'
        self.chan = Channel('ws://localhost:4000/ws')
        self.chan.join('agents:')

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

        self.chan.send('agent_update', self.get_state())

    def get_state(self):
        s = { 'agent' : self.name }
        if self.state == 'computing':
            s['progress'] = self.progress
        s['state'] = self.state
        return s



agents = []
for i in range(5):
    agents.append(Agent('Worker_{}'.format(i)))

ref = 1

while True:
    for a in agents:
        time.sleep(random.uniform(0.1, 1.5))
        a.update_state()
        s = a.get_state()
        print '{}: {}{}'.format(s['agent'], s['state'], (' (%.1f%%)' % (100.0 * s['progress'])) if s['state'] == 'computing' else '')
    print 
    print 
