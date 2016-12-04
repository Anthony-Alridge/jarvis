import brain
import ears

def volumeup():
    proc = subprocess.Popen('/usr/bin/amixer sset Master 10%+', shell=True, stdout=subprocess.PIPE)
    proc.wait()
    #speak('Turned volume up')

def volumedown():
    proc = subprocess.Popen('/usr/bin/amixer sset Master 10%-', shell=True, stdout=subprocess.PIPE)
    proc.wait()
    #speak('Turned volume down')

jarvis = brain.Brain()
jarvis.create_command(volumeup, 'louder', 2)
jarvis.create_command(volumedown, 'quieter', 3)

cl = ears.ClapDetector(jarvis)
sl = ears.SpeechListener(jarvis)

while True:
    try:
        cl.listen()
        sl.listen()
    except KeyboardInterrupt:
        cl.stop()
        sl.stop()
        sys.exit()
