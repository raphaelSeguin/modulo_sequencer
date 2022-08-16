import sys
from pyo import * 
import wx

from percs import Kick, Snare, HiHat

# MUTE
# 4 modulos
# samples

server = Server().boot().start()

app = wx.App()

class Interface(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=-1, title="I", pos=(20, 50), size=(1200, 600))
        colWidth = 50
        linHeight = 25
        instLabels = ('k', 'sn', 'hh', 'cb')
        self.instLables = [
            wx.StaticText(self, id=n, label=instLabels[n], pos=(80 + n * colWidth, 0), size=(50, 20), style=0, name="")
            for n, label in enumerate(instLabels)
        ]
        labels = ('mod1', 'mod2', 'mod3', 'offset', 'min', 'max', '_', '_')
        self.NumbersLabels = [ 
            wx.StaticText(self, id=n, label=labels[n], pos=(0, 50 + n*linHeight), 
            size=(50, 20), style=0, name="") for n in range(8)
        ]
        self.numbers = [ 
            wx.SpinCtrl(self, id=n+x*10, value="pouet", pos=(80 + x*colWidth, 50 + n*linHeight),
               size=(colWidth, 25), style=wx.SP_ARROW_KEYS, min=1, max=64, initial=8,
               name="wxSpinCtrlDouble") 
            for n in range(8)
            for x in range(4)
        ]
        [ number.Bind(wx.EVT_SPINCTRL, self.handleNumber) for number in self.numbers ]
        self.callbacks = {}

    def handleNumber(self, event):
        self.dispatch(event.GetId(), event.GetPosition())
    
    def dispatch(self, id, value):
        if id in self.callbacks:
            self.callbacks[id](value)
    
    def bind(self, id, callback):
        self.callbacks[id] = callback


class ModuloSequencer():
    def __init__(self):
        self.count = 0
        self.offset = 0
        self.modulos = [ 16 ] * 3
    
    def tick(self):
        self.count += 1

    def setModulos(self, n, value):
        self.modulos[n] = value

    def setOffset(self, value):
        self.offset = value

    @property
    def value(self):
        result = self.count + self.offset
        for modulo in self.modulos:
            result = result % modulo
        return result

class Controller():
    def __init__(self):
        self.interface = interface = Interface()
        self.interface.Show()
        self.sequencers = [ ModuloSequencer() for n in range(3) ]

        [ self.interface.bind(num + seq*10, self.makeModuloSetter(seq, num)) for num in range(3) for seq in range(4) ]

        self.interface.bind(3, self.offsetSetter0)
        self.interface.bind(13, self.offsetSetter10)

        self.sounds = [ Kick(), Snare(), HiHat() ]

        self.clock = Metro(time=0.1)
        self.clock.play()
        self.trigfunc = TrigFunc(self.clock, self.periodic)

    # modulos
    def makeModuloSetter(self, sequencer, moduloNumber):
        def moduloSetter(value):
            self.sequencers[sequencer].setModulos(moduloNumber, value)
        return moduloSetter

    # offsets
    def offsetSetter0(self, value):
        self.sequencers[0].setOffset(value)

    def offsetSetter10(self, value):
        self.sequencers[1].setOffset(value)

    def periodic(self):
        for i, sequencer in enumerate(self.sequencers): 
            sequencer.tick()
            if sequencer.value == 0:
                self.sounds[i].play()


controller = Controller()
app.MainLoop()
sys.exit()
