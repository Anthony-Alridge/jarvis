import pyttsx


def speak(text):
    engine = pyttsx.init('espeak')
    engine.setProperty('rate', 100)
    engine.say(text)
    a = engine.runAndWait()
