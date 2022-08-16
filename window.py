from pyo import *
import wx

server = Server().boot()
server.start()

app = wx.App()

class Fenetre(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=-1, title="fnetre", pos=(20, 50), size=(1200, 600))
        self.sliders = [ PyoGuiControlSlider(self, 0, 100, 50, pos=(50,i*20), size=(200, 18)) for i in range(10) ]
        self.labels = [ wx.StaticText(self, id=i, label="label {}".format(i), pos=(0, i*20),
           size=(50, 20), style=0, name="") for i in range(10)]
        
        self.vuMeter = PyoGuiVuMeter(self, nchnls=8, pos=(280, 0), size=(20, 200), orient=wx.VERTICAL, style=0)
        self.guiGrapher = PyoGuiGrapher(self, xlen=8192, yrange=(0, 1), init=[(0.0, 0.0), (1.0, 1.0)], mode=0, exp=10, inverse=True, tension=0, bias=0, pos=(400, 0), size=(200, 200), style=0)
        self.multiSlider = PyoGuiMultiSlider(self, xlen=16, yrange=(0, 1), init=None, pos=(600, 0), size=(300, 200), style=0)

        self.oscillator = Sine(200)
        self.spectrum = PyoGuiSpectrum(self, lowfreq=0, highfreq=22050, fscaling=0, mscaling=0, pos=(0, 200), size=(300, 200), style=0)
        
        self.scopeView = PyoGuiScope(self, length=0.05, gain=0.67, pos=(300, 200), size=(300, 200), style=0)
        # self.scopeView.setAnalyzer()
        self.sndTable = SndTable()

        self.sndView = PyoGuiSndView(self, pos=(600, 200), size=(300, 200), style=0)
        self.sndView.setTable(self.sndTable)
        self.sndTable.setSound('./samples/sn.wav')
        self.keyboard = PyoGuiKeyboard(self, poly=64, pos=(0, 450), size=(900, 100), style=0)

        self.numbers = [ 
            wx.SpinCtrlDouble(self, id=-1, value="", pos=(800, 200 + n*25),
               size=(50, 25), style=wx.SP_ARROW_KEYS, min=0, max=100, initial=0, inc=1,
               name="wxSpinCtrlDouble") for n in range(8)
        ]


fen = Fenetre()
fen.Show()

app.MainLoop()
