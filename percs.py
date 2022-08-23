from pyo import *


class Kick(PyoObject):
    def __init__(self, attackFreq=500, decayFreq=100, releaseFreq=50, mul=1, add=0):
        PyoObject.__init__(self, mul=1, add=0)

        self._attackFreq = attackFreq
        self._decayFreq = decayFreq
        self._releaseFreq = releaseFreq

        mul, add, lmax = convertArgsToLists(mul, add)

        self.pitchEnvelope = Expseg(
            [(0, attackFreq), (0.03, decayFreq), (0.5, releaseFreq)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=1,
        )
        self.amplitudeEnvelope = Expseg(
            [(0, 1), (0.05, 1), (0.5, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=mul,
            add=0,
        )
        self.oscillator = Sine(freq=self.pitchEnvelope, mul=self.amplitudeEnvelope)
        self._base_objs = self.oscillator.getBaseObjects()

    # def setAttackFreq(self, value):
    #     self.pitchEnvelope.set = Expseg(
    #         [(0, attackFreq), (0.03, decayFreq), (0.5, releaseFreq)],
    #         loop=False,
    #         exp=10,
    #         inverse=True,
    #         initToFirstVal=False,
    #         mul=1,
    #         add=0,
    #     )
    #     self._attackFreq = value

    # @property
    # def attackFreq(self):
    #     return self._attackFreq

    # @attackFreq.setter
    # def attackFreq(self, value):
    #     self.setAttackFreq(value)

    def play(self, dur=0, delay=0):
        self.pitchEnvelope.play(dur, delay)
        self.amplitudeEnvelope.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self.pitchEnvelope.play()
        self.amplitudeEnvelope.play()
        return PyoObject.out(self, chnl, inc, dur, delay)


##########


class Snare(PyoObject):
    def __init__(self):
        PyoObject.__init__(self, mul=1, add=0)
        self.amplitudeEnvelope = Expseg(
            [(0, 1), (0.5, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=0.8,
            add=0,
        )
        self.noise = PinkNoise(mul=self.amplitudeEnvelope)
        self.decim = Degrade(self.noise, bitdepth=4, srscale=0.1, mul=1, add=0)
        self.filter = Biquad(self.decim, freq=200, q=1, type=1, mul=1, add=0)
        self._base_objs = self.filter.getBaseObjects()

    def play(self, dur=0, delay=0):
        self.amplitudeEnvelope.play()
        return PyoObject.play(self, dur, delay)


class HiHat(PyoObject):
    def __init__(self):
        PyoObject.__init__(self, mul=1, add=0)
        self.mul = 1
        self.add = 0
        self.amplitudeEnvelope = Expseg(
            [(0, 1), (0.2, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=1,
            add=0,
        )
        self.noise = Noise(mul=self.amplitudeEnvelope)
        self.filter = Biquad(self.noise, freq=8000, q=1, type=1, mul=1, add=0)
        self._base_objs = self.filter.getBaseObjects()

    def play(self, dur=0, delay=0):
        self.amplitudeEnvelope.play()
        return PyoObject.play(self, dur, delay)


class CowBell(PyoObject):
    def __init__(self):
        PyoObject.__init__(self, mul=1, add=0)
        self.amplitudeEnvelope = Expseg(
            [(0, 1), (0.2, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=1,
            add=0,
        )
        self.fm = FM(carrier=1500, ratio=5 / 7, index=2.0, mul=self.amplitudeEnvelope)
        self._base_objs = self.fm.getBaseObjects()

    def play(self, dur=0, delay=0):
        self.amplitudeEnvelope.play()
        return PyoObject.play(self, dur, delay)


class Tom(PyoObject):
    def __init__(self, pitch):
        PyoObject.__init__(self, mul=1, add=0)
        self.amplitudeEnvelope = Expseg(
            [(0, 1), (0.5, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=1,
            add=0,
        )
        self.pitchEnvelope = Expseg(
            [(0, pitch * 3), (0.03, pitch), (0.5, pitch * 0.9)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=1,
            add=0,
        )
        self.timbreEnvelope = Expseg(
            [(0, 1), (0.03, 0.5), (0.5, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
        )
        self.oscillator = RCOsc(
            freq=self.pitchEnvelope,
            sharp=self.timbreEnvelope,
            mul=self.amplitudeEnvelope,
        )
        self._base_objs = self.oscillator.getBaseObjects()

    def play(self, dur=0, delay=0):
        self.pitchEnvelope.play()
        self.amplitudeEnvelope.play()
        self.timbreEnvelope.play()
        return PyoObject.play(self, dur, delay)


class Cym(PyoObject):
    def __init__(self):
        PyoObject.__init__(self, mul=1, add=0)
        self.amplitudeEnvelope = Expseg(
            [(0, 1), (2, 0)],
            loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=1,
            add=0,
        )
        self.noise = Noise(mul=self.amplitudeEnvelope)
        self.filter = Biquad(self.noise, freq=7000, q=1, type=1, mul=1, add=0)
        self._base_objs = self.filter.getBaseObjects()

    def play(self, dur=0, delay=0):
        self.amplitudeEnvelope.play()
        return PyoObject.play(self, dur, delay)