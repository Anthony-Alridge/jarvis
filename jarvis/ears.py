import speech_recognition as sr
import pyaudio
import audioop
#from mouth import speak
import time
import sys

class SpeechListener():
    #doesnt work well yet
    def __init__(self, brain):
        self.rec = sr.Recognizer()
        self.mic = sr.Microphone()
        self.jarvis = brain

    def handle_sound(self, recog, sound):
        try:
            command = recog.recognize_google(sound)
            print('Received ' + command)
            self.jarvis.parse_command(command, None, False)

        except sr.UnknownValueError:
            print("Could not understand audio, try again")

        except sr.RequestError as e:
            print("Recog Error; {0}".format(e))

    def listen(self):
        with self.mic as ears:
            self.rec.adjust_for_ambient_noise(ears)
        self.audio = self.rec.listen_in_background(self.mic, self.handle_sound)

    def stop(self):
        self.audio()


class ClapDetector():
    #TODO:Could I eventually use a nerual network/other magic to auto adjust the settings to good levels
    def __init__(self, brain):
        self.quietcount = 0
        self.block_counter = 0
        self.clap_counter = 0
        self.noisycount = 0
        self.rate = 44100
        self.block_time = 0.05
        self.clap_length = 0.15/self.block_time
        self.pattern_limit = 3/self.block_time #number of blocks in 3 secs
        self.block = int(self.rate*self.block_time)
        self.pa = pyaudio.PyAudio()
        self.stream = self.start_stream()
        self.background_level = self.listen_to_background()
        self.jarvis = brain



    def start_stream( self ):
        stream = self.pa.open(   format = pyaudio.paInt16,
                                 channels = 1,
                                 rate = 44100,
                                 input = True,
                                 input_device_index = None,
                                 frames_per_buffer = self.block)

        return stream

    def stop(self):
        self.stream.close()

    def listen_to_background(self):
        #try to detect how loud background is.
        print('calibrating')
        rms_values = []
        for i in range(10):
            try:
                block = self.stream.read(self.block*20) #1 second sample
                rms_values.append(audioop.rms(block, 2))
            except IOError as e:
                i -= 1
        return max(rms_values)

    def clapDetected(self):
        print('CLAP!')

    def detect_pattern(self):
        #do some action if a certain number of claps are detected in a period of time
            self.jarvis.parse_command(None, self.clap_counter, True)

    def listen(self):
        try:
            block = self.stream.read(self.block)
        except IOError as e:
            print('error')
            return
        amplitude = audioop.rms(block, 2 )

        if amplitude > self.background_level * 1.8:
            # noisy
            self.noisycount += 1
            print(self.noisycount)
            if self.noisycount  > 3/self.block_time :
                #we've had 3 seconds of noise, maybe background is louder. Recalibrate.
                self.background_level = self.listen_to_background() #TODO:Recalibrate on separate thread.
                self.noisycount = 0
        else:
            # quiet
            self.quietcount += 1
            print(self.noisycount)
            if 1 <= self.noisycount <= self.clap_length:
                #we just had a period of noisy blocks which match the length of a clap
                self.clap_counter += 1
                self.block_counter = 0 #reset pattern timer
                self.clapDetected()
            if self.quietcount > 100/self.block_time:
                self.background_level = self.listen_to_background()
                self.quietcount = 0
            self.noisycount = 0
        if self.clap_counter >= 1:
            self.block_counter += 1
        if self.block_counter >= self.pattern_limit:
            self.detect_pattern()
            self.clap_counter = 0
            self.block_counter = 0
