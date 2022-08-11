from pyo import *

s = Server().boot()

table = HarmTable([ 1 / (n+1) for n in range(12)])

lfos = [ LFO(freq=0.5 + n * 0.1, sharp=0.5, type=3, mul=3, add=0) for n in range(24)]
envelopes = [ Adsr(attack=0.01, decay=0.2, sustain=0.1, release=4, dur=5, mul=.05) for _ in range(24) ]
oscillators = [ Osc(table=table, freq=[200, 200], mul=envelopes[n]).out() for n in range(24) ]

oscillators = [ Osc(table=table, freq=[200, 200], mul=envelopes[n]).out() for n in range(24) ]

voiceNbr = 0
note = 32

def nouvelleNote():
    global voiceNbr, note
    note = ( note + 7 ) % 93
    note = note if note > 47 else note + 47
    while note % 12 not in [0, 2, 3, 5, 7, 10]:
        note += 1

    freq = midiToHz(note)
    lfo = lfos[voiceNbr]
    oscillators[voiceNbr].freq = [freq + lfo] * 2
    envelopes[voiceNbr].play()
    voiceNbr = (voiceNbr + 1) % 24


patron = Pattern(function=nouvelleNote, time=0.5)
patron.play()

s.start()
s.gui(locals())