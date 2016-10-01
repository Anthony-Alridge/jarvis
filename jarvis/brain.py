#Controls the computer
import pyautogui
import subprocess
from mouth import speak

actions = ['louder', 'quieter']

def volumeup():
    proc = subprocess.Popen('/usr/bin/amixer sset Master 10%+', shell=True, stdout=subprocess.PIPE)
    proc.wait()
    #speak('Turned volume up')

def volumedown():
    proc = subprocess.Popen('/usr/bin/amixer sset Master 10%-', shell=True, stdout=subprocess.PIPE)
    proc.wait()
    #speak('Turned volume down')

def do_action(command):
    #commands to control the volume
    if command == 'louder':
        volumeup()

    elif command == 'quieter':
        volumedown()

def parse_command(command):
        for action in actions:
            if action in command:
               do_action(action)
