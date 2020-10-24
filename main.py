import argparse
import numpy as np
import re
import sys
import time

from playsound import playsound
from scipy.io import wavfile

# Dictionary for Letters
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
# Default wav files
DOT = 'dot.wav'
DASH = 'dash.wav'


class MorseCode():
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        encoded = ""
        self.encoded = encoded

    # re-save text string as corresponding dot and dashes; print result
    def encoder(self):
        for letter in self.text:
            if(letter.islower()):
                letter = letter.upper()
            if(letter != " "):
                self.encoded += MORSE_CODE_DICT[letter] + " "
            else:
                self.encoded += " "
        print(self.encoded)

    # evaluate each char of saved encoded string; play corresponding wav file
    def encoder_to_sound(self):
        ptr = 0
        for tune in self.encoded:
            if(tune == "."):
                playsound(DOT)
            elif(tune == "-"):
                playsound(DASH)
            elif(tune == " "):
                tune = "blank"
                time.sleep(0.07)
            time.sleep(0.03)
            ptr += 1

    # create empty numpy array, dot.wav, dash.wav, 0.1s of silence, and 0.03s of silence
    # evaluate each char of saved encoded string; append corresponding numpy array; write wav file
    def encoder_to_wav(self):
        try:
            dt = np.dtype('uint8')
            blank = np.array([0] * 800, dt)   # 0.1s
            padding = np.array([0] * 240, dt) # 0.03s
            samplerate, dot = wavfile.read(DOT)
            samplerate, dash = wavfile.read(DASH)
            dot = np.append(dot, padding.copy())
            dash = np.append(dash, padding.copy())
            wav_data = np.empty((0,0), dt)
            for tune in self.encoded:
                np_data = dot.copy() if tune == '.' else dash.copy() if tune == '-' else blank.copy()
                wav_data = np.append(wav_data.copy(), np_data) 
            location = f'{self.filename}.wav'
            wavfile.write(location, samplerate, wav_data)
            print(f'{location} is ready')
        except:
            print(f'could not create {self.filename}')
            sys.exit(1)   

    # read wav file; evaluate value of wav array; save corrensponding text string
    # advance pointer position equal to the size of the matched numpy array
    def wav_to_encoder(self):
        try:    
            samplerate, wav = wavfile.read(f'{self.filename}.wav')
            end = wav.shape[0]
            self.encoded = ''
            ptr = 0
            while ptr < end: 
                if wav[ptr] == 0:
                    ptr += 800      # size of blank array
                    self.encoded += ' '
                elif wav[ptr + 800] == 128:
                    ptr += 1120     # size of dot array
                    self.encoded += '.'
                else:
                    ptr += 2080     # size of dash array
                    self.encoded += '-'
        except:
            print(f'could not read {self.filename}.wav')
            sys.exit(1)       

    # split saved encoded string into groups of dots, dashed or groups of two spaces
    # iterate through dictionary and match patterns to determine letters; text
    def decoder(self):
        cipher = re.findall(r'[.-]{1,}|[\s]{2,}', self.encoded)
        self.text = ''
        for pattern in cipher:
          if pattern == '  ':
            self.text += ' '
          else:    
            for letter, morsecode in MORSE_CODE_DICT.items():
              if pattern == morsecode:
                self.text += letter 
        print(self.text)

# create command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--wav', action='store_true', dest='wav_write', default=False, help='create a morse code wav file')
parser.add_argument('-r', '--read', action='store_true', dest='wav_read', default=False, help='decipher a morse code wav file')
parser.add_argument('-p', '--play', action='store_true', dest='wav_play', default=False, help='listen to a morse code wav file')
args = parser.parse_args()

text = ''
filename = ''
procedure = []

if args.wav_read:
    filename = input("Enter the  .wav filename: ")
    procedure.append(MorseCode.wav_to_encoder)
    procedure.append(MorseCode.decoder)
elif args.wav_write:
    text = input("Enter a message: ")
    filename = input("Enter a name for the .wav file:  ")
    procedure.append(MorseCode.encoder)
    procedure.append(MorseCode.encoder_to_wav)
elif args.wav_play:
    filename = input("Enter the  .wav filename: ")
    procedure.append(MorseCode.wav_to_encoder)
    procedure.append(MorseCode.encoder)
    procedure.append(MorseCode.encoder_to_sound)    
else:
    text = input("Enter a message: ") 
    procedure.append(MorseCode.encoder)
    procedure.append(MorseCode.encoder_to_sound)

mc = MorseCode(text, filename)
for step in procedure:
  step(mc)