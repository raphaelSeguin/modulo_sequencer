import sys, math
from pyo import * 
import wx

from percs import Kick, Snare, HiHat, CowBell, Tom, Cym
from views import SequencerView, PatternMixer

# serialize -> yml -> restore

server = Server().boot().start()

app = wx.App()

class Interface(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=-1, title="I", pos=(20, 50), size=(1200, 600))
        colWidth = 50
        linHeight = 25
        instLabels = ('k', 'sn', 'hh', 'cb', 'ht', 'mt', 'lt', 'cym')
        self.instLabels = [
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

        self.sequencerViews = [ SequencerView(self, pos=(80+n*50, 50)) for n in range(10) ]
        self.patternMixer = PatternMixer(self, pos=(800, 0))

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
        # print("setMaskModulos", n, value)
        self.maskModulos[n] = value

    def setMaskLength(self, value):
        # print("setMaskLength", value)
        self.maskLength = value

    def setMaskOffset(self, value):
        # print("setMaskOffset", value)
        self.maskOffset = value

    def setStep(self, value):
        self.step = value
    
    def setMuted(self, value):
        # print("muted", value)
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

        for sequencerView, sequencer in zip(self.interface.sequencerViews, self.sequencers):
            sequencerView.bindControl("modulo1", self.makeModuloSetter(sequencer, 0))
            sequencerView.bindControl("modulo2", self.makeModuloSetter(sequencer, 1))
            sequencerView.bindControl("modulo3", self.makeModuloSetter(sequencer, 2))
            sequencerView.bindControl("modulo4", self.makeModuloSetter(sequencer, 3))
            sequencerView.bindControl("offset", self.makeOffsetSetter(sequencer))
            sequencerView.bindControl("maskModulo1", self.makeMaskModuloSetter(sequencer, 0))
            sequencerView.bindControl("maskModulo2", self.makeMaskModuloSetter(sequencer, 1))
            sequencerView.bindControl("maskLength", self.makeMaskLengthSetter(sequencer))
            sequencerView.bindControl("maskOffset", self.makeMaskOffsetSetter(sequencer))
    
            sequencerView.bindMute(self.makeMuteSetter(sequencer))
        
        for track, sequencerView in enumerate(self.interface.sequencerViews):
            sequencerView.fader.Bind(wx.EVT_SCROLL, self.makeMixerAmpSetter(track))

        self.sounds = [ Kick(), Snare(), HiHat(), CowBell(), Tom(500), Tom(400), Tom(200), Cym() ]

        self.mixer = Mixer(outs=2, chnls=8, time=0.025, mul=0.1, add=0)

        for i, instrument in enumerate(self.sounds):
            self.mixer.addInput(i, instrument)
            self.mixer.setAmp(i, 0, 0.1)
            self.mixer.setAmp(i, 1, 0.1)
            instrument.out()

        self.mixer.out()

        self.clock = Clock(bpm=150, divisor=4)
        self.clock.play()
        self.clock.bind(self.periodic)

        # self.faderMapper = SLMap(100, 0, scale='log')

    def makeMixerAmpSetter (self, track):
        def mixerAmpSetter(event):
            db = (event.GetInt() * 0.01) * -30
            amplitude = math.pow(10, db*0.05) if event.GetInt() != 100 else 0
            self.mixer.setAmp(track, 0, amplitude)
            self.mixer.setAmp(track, 1, amplitude)
        return mixerAmpSetter

    # modulos
    def makeModuloSetter(self, sequencer, moduloNumber):
        def moduloSetter(value):
            sequencer.setModulos(moduloNumber, value)
        return moduloSetter
    # offsets
    def makeOffsetSetter(self, sequencer):
        def offsetSetter(value):
            sequencer.setOffset(value)
        return offsetSetter

    def makeMaskModuloSetter(self, sequencer, moduloNumber):
        def maskModuloSetter(value):
            sequencer.setMaskModulos(moduloNumber, value)
        return maskModuloSetter

    def makeMaskLengthSetter(self, sequencer):
        def maskLengthSetter(value):
            sequencer.setMaskLength(value)
        return maskLengthSetter

    def makeMaskOffsetSetter(self, sequencer):
        def maskOffsetSetter(value):
            sequencer.setMaskOffset(value)
        return maskOffsetSetter

    def makeMuteSetter(self, sequencer):
        def muteSetter(value):
            sequencer.setMuted(value)
        return muteSetter

    def periodic(self, count):
        for i, sequencer in enumerate(self.sequencers):
            sequencer.setStep(count)
            if sequencer.trigger:
                self.sounds[i].play()



controller = Controller()

app.MainLoop()

sys.exit()
