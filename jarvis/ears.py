import speech_recognition as sr
from brain import parse_command
from mouth import speak
import time
import sys


def handle_sound(recog, sound):
        try:
            command = recog.recognize_google(sound)
            print('Received ' + command)
            speak('Received' + command)
            parse_command(command)

        except sr.UnknownValueError:
            print("Could not understand audio, try again")

        except sr.RequestError as e:
            print("Recog Error; {0}".format(e))    
        

def listen():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.energy_threshold = 4000
    rec.dynamic_energy_threshold = True
    with mic as ears:
        speak('Listening to background')
        rec.adjust_for_ambient_noise(ears, duration=5)
        print('Listening')
        audio = rec.listen(ears)
    handle_sound(rec, audio)
    while True:
        try:
            listen()
        except KeyboardInterrupt:
            sys.exit()
            
listen()
'''
import speech_recognition as sr

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
import time
for _ in range(50): time.sleep(0.1) # we're still listening even though the main thread is doing other things
stop_listening() '''
