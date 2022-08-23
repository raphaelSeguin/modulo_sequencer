import wx

# Position = tuple[int, int]

class SequencerView():
    def __init__(self, parent, pos=(0, 0)):
        self.controlValues = [
            {
                "name": "modulo1",
                "min": 1,
                "max": 64,
                "initial": 64,
            },
            {
                "name": "modulo2",
                "min": 1,
                "max": 64,
                "initial": 32,
            },
            {
                "name": "modulo3",
                "min": 1,
                "max": 64,
                "initial": 16,
            },
            {
                "name": "modulo4",
                "min": 1,
                "max": 64,
                "initial": 8,
            },
            {
                "name": "offset",
                "min": 0,
                "max": 64,
                "initial": 0,
            },
            {
                "name": "maskModulo1",
                "min": 1,
                "max": 64,
                "initial": 16,
            },
            {
                "name": "maskModulo2",
                "min": 1,
                "max": 64,
                "initial": 16,
            },
            {
                "name": "maskLength",
                "min": 0,
                "max": 64,
                "initial": 16,
            },
            {
                "name": "maskOffset",
                "min": 0,
                "max": 64,
                "initial": 0,
            }
        ]
        self.controls = [
            wx.SpinCtrl(
                parent, 
                id=n,
                pos=(pos[0], pos[1] + n*25),
                size=(50, 25),
                style=wx.SP_ARROW_KEYS,
                **self.controlValues[n],
            ) for n in range(9)
        ]
        for control in self.controls:
            control.Bind(wx.EVT_SPINCTRL, self.spinCtrlHandler)

        self.mute = wx.ToggleButton(
            parent,
            id=10,
            label="",
            pos=(pos[0], pos[1] + 225),
            size=(50, 25),
        )
        self.fader = wx.Slider(
            parent,
            id=20,
            value=20,
            minValue=0,
            maxValue=100,
            pos=(pos[0], pos[1] + 250),
            size=(50, 100),
            style=wx.SL_VERTICAL,
            name=""
        )
        self.mute.Bind(wx.EVT_TOGGLEBUTTON, self.muteButtonHandler)
        self.fader.Bind(wx.EVT_SLIDER, self.faderHandler)
        self.callbacks = {}

    def spinCtrlHandler(self, event):
        id = event.GetId()
        if id in self.callbacks:
            self.callbacks[id](event.GetPosition())
    
    def muteButtonHandler(self, event):
        if 'mute' in self.callbacks:
            self.callbacks['mute'](bool(event.GetInt()))

    def faderHandler(self, event):
        if 'fader' in self.callbacks:
            self.callbacks['fader'](event.GetPosition())

    def bindControl(self, name, function):
        assert(name in [ control['name'] for control in self.controlValues ])
        assert(name not in self.callbacks)
        index = list(map(lambda obj: obj['name'], self.controlValues)).index(name)
        self.callbacks[index] = function

    def bindMute(self, function):
        self.callbacks['mute'] = function

    def bindFader(self, function):
        self.callbacks['fader'] = function

class PatternMixer():
    def __init__(self, parent, pos=(0, 0)):
        self.patternChoiceA = wx.Choice(parent, id=wx.ID_ANY, pos=(pos[0], pos[1]), size=wx.DefaultSize,
            choices=[str(n) for n in range(10)], style=0, name="")
        self.patternChoiceB = wx.Choice(parent, id=wx.ID_ANY, pos=(pos[0] + 50, pos[1]), size=wx.DefaultSize,
            choices=[str(n) for n in range(10)], style=0, name="")
        self.patternCrossfader = wx.Slider(parent, id=wx.ID_ANY, value=20, minValue=0, maxValue=100,
                pos=(pos[0], pos[1]+ 25), size=(80, 20), style=wx.SL_HORIZONTAL,
                name="")