import brain
import ears
from standard import browser

jarvis = brain.Brain()
jarvis.add(browser)


cl = ears.ClapDetector()
sl = ears.SpeechListener()

manager = ears.InterfaceManager([cl, sl], jarvis)


manager.run()

while True:
    try:
       manager.process_commands()
    except KeyboardInterrupt:
        manager.stop()
        sys.exit()
