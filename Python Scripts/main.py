from playsound import playsound
import time

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

# Helper Functions :)

def dot():
    playsound('dot.wav')

def dash():
    playsound('dash.wav')

class MorseCode():
    def __init__(self, text):
        self.text = text
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
                dot()
            elif(tune == "-"):
                dash()
            elif(tune == " "):
                tune = "blank"
                time.sleep(0.07)
            time.sleep(0.03)
            ptr += 1


text = input("Enter a letter: ")
t1 = MorseCode(text)
t1.encoder()
t1.encoder_to_sound()
