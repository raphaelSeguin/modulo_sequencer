import sys
from pyo import * 
import wx

from percs import Kick, Snare, HiHat, CowBell, Tom, Cym

# serialize -> yml -> restore

server = Server().boot().start()

app = wx.App()

class Interface(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=-1, title="I", pos=(20, 50), size=(1200, 600))
        colWidth = 50
        linHeight = 25
        cols = 8
        self.patternChoiceA = wx.Choice(self, id=wx.ID_ANY, pos=(80 + 8*colWidth, 0), size=wx.DefaultSize,
            choices=[str(n) for n in range(10)], style=0, name="")
        self.patternChoiceB = wx.Choice(self, id=wx.ID_ANY, pos=(80 + 9*colWidth, 0), size=wx.DefaultSize,
            choices=[str(n) for n in range(10)], style=0, name="")
        self.patternCrossfader = wx.Slider(self, id=wx.ID_ANY, value=20, minValue=0, maxValue=100,
                pos=(80 + 8*colWidth, 25), size=(80, 20), style=wx.SL_HORIZONTAL,
                name="")
        instLabels = ('k', 'sn', 'hh', 'cb', 'ht', 'mt', 'lt', 'cym')
        self.instLables = [
            wx.StaticText(self, id=n, label=instLabels[n], pos=(80 + n * colWidth, 0), size=(50, 20), style=0, name="")
            for n, label in enumerate(instLabels)
        ]
        labels = ('mod1', 'mod2', 'mod3', 'mod4', 'offset', 'mmod1', 'mmod2', 'mlength', 'moffset', 'mute', 'faders')
        defaultValues = ( 32, 16, 8, 4, 0, 16, 16, 16, 0 )
        self.NumbersLabels = [ 
            wx.StaticText(self, id=n, label=labels[n], pos=(0, 50 + n*linHeight), 
                size=(50, 20), style=0, name="")
            for n in range(len(labels))
        ]
        self.numbers = [ 
            wx.SpinCtrl(self, 
                id=row+col*10,
                pos=(80 + col*colWidth, 50 + row*linHeight),
                size=(colWidth, 25),
                style=wx.SP_ARROW_KEYS,
                min=0,
                max=64,
                initial=defaultValues[row],
                name="wxSpinCtrlDouble_{row}_{col}".format(row=row, col=col)) 
            for row in range(9)
            for col in range(cols)
        ]
        [ number.Bind(wx.EVT_SPINCTRL, self.handleNumber) for number in self.numbers ]
        self.muteButtons = [
            wx.ToggleButton(
                self,
                id=7+(col+1)*100,
                label="",
                pos=(80 + col*colWidth, 50 + 9*linHeight),
                size=(50, 20),
            )
            for col in range(cols)
        ]
        [ muteButton.SetValue(1) for muteButton in self.muteButtons ]
        [ muteButton.Bind(wx.EVT_TOGGLEBUTTON, self.handleMuteButtons) for muteButton in self.muteButtons ]
        self.faders = [
            wx.Slider(self, id=wx.ID_ANY, value=20, minValue=0, maxValue=100,
                pos=(80 + col*colWidth, 50 + 10*linHeight), size=(colWidth, 100), style=wx.SL_VERTICAL,
                name="")
            for col in range(cols)
        ]
        self.callbacks = {}

    def handleNumber(self, event):
        self.dispatch(event.GetId(), event.GetPosition())
    
    def handleMuteButtons(self, event):
        self.dispatch(event.GetId(), bool(event.GetInt()))
    
    def dispatch(self, id, value):
        if id in self.callbacks:
            self.callbacks[id](value)
    
    def bind(self, id, callback):
        self.callbacks[id] = callback


class ModuloSequencer():
    def __init__(self):
        self.modulos = [32, 16, 8, 4]
        self.offset = 0
        self.maskModulos = [16, 16]
        self.maskLength = 16
        self.maskOffset = 0
        self.muted = True

    def setModulos(self, n, value):
        self.modulos[n] = value

    def setOffset(self, value):
        self.offset = value

    def setMaskModulos(self, n, value):
        print("setMaskModulos", n, value)
        self.maskModulos[n] = value

    def setMaskLength(self, value):
        print("setMaskLength", value)
        self.maskLength = value

    def setMaskOffset(self, value):
        print("setMaskOffset", value)
        self.maskOffset = value

    def setStep(self, value):
        self.step = value
    
    def setMuted(self, value):
        print("muted", value)
        self.muted = value

    @property
    def value(self):
        result = self.step + self.offset
        for modulo in self.modulos:
            result %= modulo
        return result

    @property
    def mask(self):
        maskStep = self.step + self.maskOffset
        for modulo in self.maskModulos:
            maskStep %= modulo
        return maskStep < self.maskLength

    @property
    def trigger(self):
        if self.value == 0 and self.mask and not self.muted:
            return True
        else:
            return False

class Clock():
    def __init__(self, bpm=150, divisor=4):
        time = 60 / (bpm * divisor)
        self.metro = Metro(time=time)
        self.count = 0
        
    def play(self):
        self.metro.play()

    def bind(self, function):
        self.callback = function
        self.trig = TrigFunc(self.metro, self.tick)

    def unbind(self):
        self.callback = None

    def tick(self):
        self.count += 1
        if self.callback:
            self.callback(self.count)


class Controller():
    def __init__(self):
        self.interface = Interface()
        self.interface.Show()
        sequencersNumber = 8
        self.sequencers = [ ModuloSequencer() for n in range(sequencersNumber) ]
        [ self.interface.bind(0 + num + seq*10, self.makeModuloSetter(seq, num)) for num in range(4) for seq in range(sequencersNumber) ]
        [ self.interface.bind(4 + seq*10, self.makeOffsetSetter(seq)) for seq in range(sequencersNumber) ]
        [ self.interface.bind(5 + num + seq*10, self.makeMaskModuloSetter(seq, num)) for num in range(2) for seq in range(sequencersNumber) ]
        [ self.interface.bind(7 + seq*10, self.makeMaskLengthSetter(seq)) for seq in range(sequencersNumber) ]
        [ self.interface.bind(8 + seq*10, self.makeMaskOffsetSetter(seq)) for seq in range(sequencersNumber) ]
        [ self.interface.bind(7 + seq*100, self.makeMuteSetter(seq)) for seq in range(1, sequencersNumber+1) ]
#
#     ! ! ! ! !
#
        # for seq, button in enumerate(self.interface.muteButtons):
        #     print(button)
        #     button.Bind(wx.EVT_TOGGLEBUTTON, self.makeMuteSetter(seq))
#

#
        self.sounds = [ Kick(), Snare(), HiHat(), CowBell(), Tom(500), Tom(400), Tom(200), Cym() ]

        self.clock = Clock(bpm=150, divisor=4)
        self.clock.play()
        self.clock.bind(self.periodic)
    # modulos
    def makeModuloSetter(self, sequencer, moduloNumber):
        def moduloSetter(value):
            self.sequencers[sequencer].setModulos(moduloNumber, value)
        return moduloSetter
    # offsets
    def makeOffsetSetter(self, sequencer):
        def offsetSetter(value):
            self.sequencers[sequencer].setOffset(value)
        return offsetSetter
    # maskModulos
    def makeMaskModuloSetter(self, sequencer, moduloNumber):
        def maskModuloSetter(value):
            self.sequencers[sequencer].setMaskModulos(moduloNumber, value)
        return maskModuloSetter
    # maskLength
    def makeMaskLengthSetter(self, sequencer):
        def maskLengthSetter(value):
            self.sequencers[sequencer].setMaskLength(value)
        return maskLengthSetter
    # maskOffset
    def makeMaskOffsetSetter(self, sequencer):
        def maskOffsetSetter(value):
            self.sequencers[sequencer].setMaskOffset(value)
        return maskOffsetSetter
    # mutes
    def makeMuteSetter(self, sequencer):
        def muteSetter(value):
            # print(sequencer, value)
            self.sequencers[sequencer].setMuted(value)
        return muteSetter

    def periodic(self, count):
        # self.interface.stepDisplay.SetValue(str(count))
        for i, sequencer in enumerate(self.sequencers): 
            sequencer.setStep(count)
            if sequencer.trigger:
                self.sounds[i].play()

controller = Controller()

app.MainLoop()
sys.exit()
