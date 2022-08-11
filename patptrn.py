from typing import Pattern
from pyo import *
from random import uniform

s = Server().boot()

env = Adsr(attack=0.0001, decay=0.1, sustain=0., release=.0, dur=0.2, mul=0.3)
osc = RCOsc(freq=[200, 200], mul=env).out(0)

class Patternalist():
    def __init__(self):
        self.time = 0
        self._rightFreq = 0
        self._leftFreq = 0
    
    def tick(self):
        self.time += 1

    def leftFreq(self):
        if self.time % 27 == 0: 
            self._leftFreq = 23
        self._leftFreq = self._leftFreq * 3/2 if self._leftFreq < 2000 else self._leftFreq - 1800
        return self._leftFreq

    def rightFreq(self):
        if self.time % 29 == 0: 
            self._rightFreq = 19
        self._rightFreq = self._rightFreq * 5/3 if self._rightFreq < 2000 else self._rightFreq - 1800
        return self._rightFreq

pouet = Patternalist()

def event():
    osc.freq = [ pouet.leftFreq(), pouet.rightFreq() ]
    pouet.tick()
    if pouet.time % 7 != 0: env.play()

pat = Pattern(function=event, time=.08)
pat.play()

s.gui(locals())