from pyo import *

s = Server().boot()

s.start()

f = s.getSamplingRate() / 262144

move = LinTable([(0, 2.), (8191, 0.2)])
bend = TableRead(table=move, freq=1/10, loop=True).play()

t = PadSynthTable(basefreq=50, spread=1.5, bw=10., bwscl=1., nharms=128, damp=0.7, size=262144)

a = Osc(table=t, freq=f * bend, phase=0, mul=0.5).mix(1)
b = a.mix(1).out(0)
a.out(1)

s.gui(locals())