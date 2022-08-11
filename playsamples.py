from pyo import *

server = Server().boot()

initStepTime = 0.3
stepTime = initStepTime

# # avec OSC et SndTable
# snd1 = SndTable(path='./samples/k.wav', chnl=0, stop=0.1)
# freq = snd1.getRate()
# player = Osc(table=snd1, freq=[freq] * 2, mul=0.2).out()

# avec TableRead
sounds = ['k', 'hh', 'sn', 'cb']
sndz = [ SndTable(path='./samples/' + sound + '.wav', chnl=0) for sound in sounds]

count = 0
step = 0
player = TableRead(table=sndz[0], freq=[0, 0], loop=False, mul=.3).out()

lfo = Sine(freq=0.13, mul=0.012, add=0.013)
lfo2 = LFO(freq=5, sharp=0.5, type=6, mul=0.01, add=0.011)
delay = Delay(player, delay=lfo+lfo2, feedback=0.5, maxdelay=1, mul=1, add=0).out()

def delayTypeGenerator():
    while True:
        for val in [0, 4, 6]:
            yield val

delayType = delayTypeGenerator()

def bump():
    global count, step, stepTime
    step = count % 4
    if step == 0:
        delay.type = delayType.__next__()
        delay.delay = stepTime / 2
        delay.mul = 1.
        delay.feedback = 0.
    elif step == 2:
        delay.delay = stepTime / 2
        delay.feedback = 0.
        delay.mul = 1
    elif step == 3:
        delay.delay = lfo + lfo2
        delay.feedback = 0.9
        stepTime *= 0.9
    else:
        delay.delay = lfo + lfo2
        delay.feedback = 0.5
        delay.mul = 1
    player.table = sndz[step]
    player.freq = [sndz[step].getRate()] * 2
    player.play()
    player.out()
    count += 1
    if stepTime < 0.01:
        stepTime = initStepTime
    pat.time = stepTime


pat = Pattern(function=bump, time=stepTime)
pat.play()

server.gui(locals())