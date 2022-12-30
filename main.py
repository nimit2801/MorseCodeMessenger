import argparse
import numpy as np
import re
import sys
import time

from scipy.io import wavfile
import winsound

# Dictionary for Letters
DOT = 'dot.wav'
DASH = 'dash.wav'
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

class MorseCode():
    def __init__(self, text, filename):
        self.text = text
        self.filename = filename
        encoded = ""
        self.encoded = encoded

    def encoder(self):
        for letter in self.text:
            if(letter.islower()):
                letter = letter.upper()
            if(letter != " "):
                self.encoded += MORSE_CODE_DICT[letter] + " "
            else:
                self.encoded += " "
        print(self.encoded)

    def encoder_to_sound(self):
        ptr = 0
        for tune in self.encoded:
            if(tune == "."):
                winsound.PlaySound(DOT, winsound.SND_FILENAME)
            elif(tune == "-"):
                winsound.PlaySound(DASH, winsound.SND_FILENAME)
            elif(tune == " "):
                tune = "blank"
                time.sleep(0.07)
            time.sleep(0.03)
            ptr += 1

    def encoder_to_wav(self):
        try:
            dt = np.dtype('uint8')
            blank = np.array([0] * 240, dt)
            samplerate, dot = wavfile.read(DOT)
            samplerate, dash = wavfile.read(DASH)
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

    def wav_to_encoder(self):
        try:    
            samplerate, wav = wavfile.read(f'{self.filename}.wav')
            end = wav.shape[0]
            self.encoded = ''
            ptr = 0
            while ptr < end: 
                if wav[ptr] == 0:
                    ptr += 240
                    self.encoded += ' '
                elif wav[ptr + 800] == 128:
                    ptr += 880
                    self.encoded += '.'
                else:
                    ptr += 1840
                    self.encoded += '-'
        except:
            print(f'could not read {self.filename}.wav')
            sys.exit(1)       

    def decoder(self):
        cipher = re.findall(r'[.-]{1,}|[\s]{2,}', self.encoded)
        text = ''
        for pattern in cipher:
          if pattern == '  ':
            text += ' '
          else:    
            for letter, morsecode in MORSE_CODE_DICT.items():
              if pattern == morsecode:
                text += letter 
        print(text)

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