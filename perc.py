from pyo import *

s = Server().boot()
# KICK KICK

class Kick:
    def __init__(self):
        self.pitchEnvelope = Expseg([(0, 500), (0.03, 100), (0.5, 50)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
        self.amplitudeEnvelope = Expseg([(0, 1), (0.05, 1), (0.5, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
        self.oscillator = Sine(freq=self.pitchEnvelope, mul=self.amplitudeEnvelope).mix(2).out()

    def play(self):
        self.oscillator.reset()
        self.pitchEnvelope.play()
        self.amplitudeEnvelope.play()

class Snare:
    def __init__(self):
        self.amplitudeEnvelope = Expseg([(0, 1), (0.095, 1), (0.1, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)

    def play(self):
        self.noise = PinkNoise(mul=self.amplitudeEnvelope)
        self.decim = Degrade(self.noise, bitdepth=4, srscale=0.1, mul=1, add=0)
        self.filter = Biquad(self.decim, freq=200, q=1, type=1, mul=1, add=0).mix(2).out()
        self.amplitudeEnvelope.play()

step = 0
kick = Kick()
snare = Snare()

def bang():
    global kick, snare, step
    if step == 0: kick.play()
    if step == 1: snare.play()
    step = (step + 1) % 2

pat = Pattern(function=bang, time=0.601)
pat.play()

s.gui(locals())