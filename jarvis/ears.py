import speech_recognition as sr
import pyaudio
import audioop
#from mouth import speak
import time
import sys
from abc import ABCMeta, abstractmethod
from threading import thread

class Interface(metaclass=ABCMeta):
    #Base class for interfaces (ways to interact with Jarvis)
    @abstractmethod
    def run():
        pass

    @abstractmethod
    def stop():
        pass

    @abstractmethod
    def get_command():
        pass

class SpeechListener(Interface):
    #doesnt work well yet
    def __init__(self):
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.commands = []

    def handle_sound(self, recog, sound):
        try:
            command = recog.recognize_google(sound)
            print('Received ' + command)

        except sr.UnknownValueError:
            print("Could not understand audio, try again")

        except sr.RequestError as e:
            print("Recog Error; {0}".format(e))

    def run(self):
        with self.mic as ears:
            self.rec.adjust_for_ambient_noise(ears)
        self.audio = self.rec.listen_in_background(self.mic, self.handle_sound)

    def stop(self):
        self.audio()

    def get_command(self):
        if self.commands:
            return self.commands.pop(0)
        return None


class ClapDetector(Interface):
    #TODO:Could I eventually use a nerual network/other magic to auto adjust the settings to good levels
    def __init__(self):
        #Get rid of magic numbers
        #initialising variables
        self.block_counter = 0
        self.clap_counter = 0
        self.commands = []
        self.quietcount = 0
        self.noisycount = 0
        #settings
        self.block_time = 0.05
        self.clap_length = 0.15/self.block_time
        self.rate = 44100
        self.block = int(self.rate * self.block_time)
        self.pattern_limit = 3/self.block_time  #number of blocks in 3 secs
        self.sensitivity = 1.8
        #initialising objects
        self.pa = pyaudio.PyAudio()
        self.stream = self.start_stream()
        self.background_level = self.listen_to_background()

    def start_stream(self):
        stream = self.pa.open(format = pyaudio.paInt16,
                              channels = 1,
                              rate = self.rate,
                              input = True,
                              input_device_index = None,
                              frames_per_buffer = self.block)
        return stream

    def stop(self):
        self.stream.close()

    def listen_to_background(self):
        #try to detect how loud background is.
        rms_values = []
        for i in range(10):
            try:
                block = self.stream.read(self.block * 20) #1 second sample
                rms_values.append(audioop.rms(block, 2))
            except IOError as e:
                i -= 1
        return max(rms_values)

    def claps_detected(self):
        print("activity in clap detector")
        self.commands.append(self.clap_counter)

    def run(self):
        try:
            block = self.stream.read(self.block)
        except IOError as e:
            print(e)
            return

        amplitude = audioop.rms(block, 2 )

        if amplitude > self.background_level * self.sensitivity:
            # noisy
            self.noisycount += 1
            print(self.noisycount)
            if self.noisycount  > 3 / self.block_time :
                #we've had 3 seconds of noise, maybe background is louder. Recalibrate.
                self.background_level = self.listen_to_background()
                self.noisycount = 0
        else:
            # quiet
            self.quietcount += 1
            if 1 <= self.noisycount <= self.clap_length:
                #we just had a period of noisy blocks which match the length of a clap
                self.clap_counter += 1
                self.block_counter = 0 #reset pattern timer
            if self.quietcount > 100/self.block_time:
                self.background_level = self.listen_to_background()
                self.quietcount = 0
            self.noisycount = 0
        if self.clap_counter >= 1:
            self.block_counter += 1
        if self.block_counter >= self.pattern_limit:
            self.claps_detected()
            self.clap_counter = 0
            self.block_counter = 0

    def get_command(self):
        if self.commands:
            return self.commands.pop(0)
        return None

class Terminal(Interface, Thread):

    def __init__(self):
        self.commands = []

    def run():
        while True:
            command = input()
            if command:
                self.commands.append(command)

    def stop():
        pass

    def get_command():
        #Duplicating a lot of code...
        if self.commands:
            return self.commands.pop(0)
        return None

class InterfaceManager:

    def __init__(self, interfaces, jarvis):
        self.interfaces = interfaces
        self.jarvis = jarvis

    def run(self):
        for interface in self.interfaces:
            interface.run()

    def stop(self):
        for interface in self.interfaces:
            interface.stop()

    def process_commands(self):
        for interface in self.interfaces:
            self.jarvis.parse_command(interface.get_command())
