# jarvis
A simple tool which allows the user to create commands to control their computers and a spoken command or certain number of claps to activate their function. "Jarvis" will handle recognising speech (using SpechRecognition library) and claps and matching these to the supplied functions. In the futrue I am to include pattern recognition on claps and to supply common commands which a user may want enabled to control their computer. Perhaps also include a command line interface for talking to Jarvis.

Example usage:
 ```python
 import brain
 import ears
 
 jarvis = brain.Brain()
 jarvis.create_command(volumeup, "louder", 1)
 #Will turn volume up if user says louder or claps once, for some volumeup function defined by user.
 cl = ears.ClapListener(jarvis)
 sl = ears.SpeechListener(jarvis)
#pass in jarvis so that our listens can access the commands.
while True:
    try:
      cl.listen()
      sl.listen()
    except KeyBoardInterrupt:
      cl.stop()
      sl.stop()
      sys.exit()
  
 ```
