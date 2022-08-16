from pyo import *
import os

server = Server().boot()

class Sampler():
    def __init__(self, directory='./samples'):
        [ print(sample) for sample in os.listdir(directory) ]
        self.samples = [ SndTable(path=directory + '/' + sample, chnl=0) for sample in os.listdir(directory)]
        self.tables = [ TableRead(table=table, freq=[2, 2], loop=False) for table in self.samples ]
    
    def play(self, n):
        self.tables[n].play()
        self.tables[n].out()

sampler = Sampler(directory='./samples')

def pouet(n):
    global sampler
    sampler.play(n)

phase = Sine(1)

bing = TrigFunc(
    TrigBurst(
        Thresh(
            phase, 
            threshold=-0.5,
            dir=1
        ),
        time=0.1, count=10, expand=0.9
    ),
    pouet, arg=0)
snare = TrigFunc(Thresh(phase, threshold=0.9, dir=0), pouet, arg=3)
kick = TrigFunc(Thresh(phase, threshold=0.2, dir=0), pouet, arg=1)

server.gui(locals())