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
        self.amplitudeEnvelope = Expseg([(0, 1), (0.5, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=0.8, add=0)

    def play(self):
        self.noise = PinkNoise(mul=self.amplitudeEnvelope)
        self.decim = Degrade(self.noise, bitdepth=4, srscale=0.1, mul=1, add=0)
        self.filter = Biquad(self.decim, freq=200, q=1, type=1, mul=1, add=0).mix(2).out()
        self.amplitudeEnvelope.play()

class HiHat:
    def __init__(self):
        self.amplitudeEnvelope = Expseg([(0, 1), (0.2, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)

    def play(self):
        self.noise = Noise(mul=self.amplitudeEnvelope)
        self.filter = Biquad(self.noise, freq=8000, q=1, type=1, mul=1, add=0).mix(2).out()
        self.amplitudeEnvelope.play()

class CowBell:
    def __init__(self):
        self.amplitudeEnvelope = Expseg([(0, 1), (0.2, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)

    def play(self):
        self.fm = FM(carrier=1500, ratio=5/7, index=2., mul=self.amplitudeEnvelope).mix(2).out()
        self.amplitudeEnvelope.play()

class Tom():
    def __init__(self, pitch):
        self.amplitudeEnvelope = Expseg([(0, 1), (0.5, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
        self.pitchEnvelope = Expseg([(0, pitch * 3), (0.03, pitch), (0.5, pitch*0.9)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
        self.timbreEnvelope = Expseg([(0, 1), (0.03, 0.5), (0.5, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False)
    def play(self):
        self.oscillator = RCOsc(freq=self.pitchEnvelope, sharp=self.timbreEnvelope ,mul=self.amplitudeEnvelope).mix(2).out()
        self.pitchEnvelope.play()
        self.amplitudeEnvelope.play()
        self.timbreEnvelope.play()

class Cym():
    def __init__(self):
        self.amplitudeEnvelope = Expseg([(0, 1), (2, 0)], loop=False, exp=10, inverse=True, initToFirstVal=False, mul=1, add=0)
    
    def play(self):
        self.noise = Noise(mul=self.amplitudeEnvelope)
        self.filter = Biquad(self.noise, freq=7000, q=1, type=1, mul=1, add=0).mix(2).out()
        self.amplitudeEnvelope.play()