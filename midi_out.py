from pyo import *

s = Server()
s.deactivateMidi()
s.boot()

dispatch = MidiDispatcher(4)
dispatch.start()

def ping():
    global dispatch
    dispatch.send(144, 60, 127)

pat = Pattern(function=ping, time=0.5)
pat.play()

s.start()
s.gui(locals())