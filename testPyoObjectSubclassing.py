from pyo import *
from percs import Kick
import wx

app = wx.App()

class Fenetre(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=-1, title="TEST", pos=(20, 20), size=(200, 200))
        
class TestInstru(PyoObject):
    def __init__(self, mul=0.1):
        PyoObject.__init__(self)
        self.env = Expseg([(0, 1), (10, 0)], loop=False,
            exp=10,
            inverse=True,
            initToFirstVal=False,
            mul=mul,)
        self.oscil = Sine(300, mul=self.env)
        self._base_objs = self.oscil.getBaseObjects()

    def play(self, dur=0, delay=0):
        self.env.play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self.env.play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)


server = Server().boot().start()

instr = TestInstru()
kick = Kick(attackFreq=5000)

mix = Mixer(outs=2, chnls=2, time=0.025)
mix.addInput(0, instr)
mix.setAmp(0,0,.5)
mix.addInput(1, kick)
mix.setAmp(1,0,.5)
mix.out()

def pouet():
    global instr, kick
    instr.play()
    kick.play()

pattern = Pattern(function=pouet, time=1)
pattern.play()

fenetre = Fenetre()
# fenetre.Show()

app.MainLoop()