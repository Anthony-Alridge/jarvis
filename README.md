# jarvis
A simple tool which allows the user to create commands to control their computers and a spoken command or certain number of claps to activate their function. "Jarvis" will handle recognising speech (using SpechRecognition library) and claps and matching these to the supplied functions. In the futrue I am to include pattern recognition on claps and to supply common commands which a user may want enabled to control their computer. Perhaps also include a command line interface for talking to Jarvis.

Example usage:
 ```python
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
  
 ```

The above will supply some commands sucj as "volume up" to turn laptops volume up.
