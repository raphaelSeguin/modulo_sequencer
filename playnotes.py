from pyo import *

s = Server().boot()

voiceNbr = 0
note = 32
step = 0
stepTime = 0.125

lfos = [ LFO(freq=0.5 + n * 0.1, sharp=0.5, type=3, mul=3, add=0) for n in range(24)]
panlfos = [ LFO(freq=0.5 + n * 0.1, sharp=0.5,type=3, mul=0.25, add=0.5) for n in range(24)]

envelopes = [ Adsr(attack=0.005, decay=0.2, sustain=0.1, release=4, dur=5, mul=.05) for _ in range(24) ]
sharp_envelopes = [ Adsr(attack=0.025, decay=0.4, sustain=0.1, release=4, dur=5, mul=.8) for _ in range(24) ]

# oscillators = [ Osc(table=table, freq=[200, 200], mul=envelopes[n]) for n in range(24) ]
oscillators = [ RCOsc( freq=[200, 200],sharp=sharp_envelopes[n] + lfos[n] * 0.05, mul=envelopes[n]) for n in range(24) ]
pans = [ Pan(oscillators[n], outs=2, pan=panlfos[n], spread=0.).out() for n in range(24) ]

mixer = Mixer(outs=2, chnls=24, time=.025)
for n in range(24):
    mixer.addInput(n, pans[n])
    mixer.setAmp(n, 0, 0.5)
    mixer.setAmp(n, 1, 0.5)
stereo_delay = [ Delay(mixer[i], delay=stepTime * (5 + i*2), feedback=0.3, maxdelay=1, mul=0.3, add=0).out(i) for i in range(2)]
stereo_reverb = [ Freeverb(mixer[i] , size=.9, damp=.5, mul=.5).out() for i in range(2) ]

def nouvelleNote():
    global voiceNbr, note, step, stepTime
    note = ( note + 7 ) % (73 + (step % 11))
    note = note if note > 47 else note + 47
    playnote = note
    while playnote % 12 not in [0, 2, 3, 5, 7, 10]:
        playnote += 1
    freq = midiToHz(playnote)
    lfo = lfos[voiceNbr]
    oscillators[voiceNbr].freq = [freq + lfo] * 2
    envelopes[voiceNbr].play()
    sharp_envelopes[voiceNbr].play()
    voiceNbr = (voiceNbr + 1) % 24
    patron.time = ((int(step**3.5) % 4) + 1) * stepTime
    step += 1


patron = Pattern(function=nouvelleNote, time=0.5)
patron.play()

s.start()
s.gui(locals())