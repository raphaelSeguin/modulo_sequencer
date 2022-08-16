from pyo import *

class Kick:
    def __init__(self):
        self.pitchEnvelope = Expseg([(0, 500), (0.03, 100), (0.5, 50)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
        self.amplitudeEnvelope = Expseg([(0, 1), (0.05, 1), (0.5, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
        
    def play(self):
        self.oscillator = Sine(freq=self.pitchEnvelope, mul=self.amplitudeEnvelope).mix(2).out()
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