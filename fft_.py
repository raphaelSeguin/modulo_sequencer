from pyo import *

server = Server().boot()
server.start()

lfo = LFO(1, mul=10000, add=10000)
a = Noise(0.5).mix(2)

fin = FFT(a, size=1024, overlaps=4, wintype=2)

t = ExpTable(list=[(0,0), (199, 0), (200, 1), (220, 1), (221, 0), (1023,0)], exp=10, inverse=True, size=1024)

amp = TableIndex(t, fin["bin"])

re = fin["real"] * amp
im = fin["imag"] * amp

scope = Scope(amp, length=0.05, gain=0.67, function=None, wintitle='Scope')
sizeLfo = LFO(0.2, mul=8, add=8)
fout = IFFT(re, im, size=1024, overlaps=4, wintype=2).mix(2).out()
spectrum = Spectrum(fout, size=1024, wintype=2, function=None, wintitle='Spectrum')

server.gui(locals())