# MorseCodeMessenger
This Project will currently let you convert your text into Encrypted Morse Code with audio!
##Usage
```
>>> python main.py
Enter a message:
```
Optional flags | Purpose| Example
--|--|--
`-w`<br>`--wav` | Create a Morse Code audio file | At the prompts, enter a message *Hello World* and a name *hi*. An audio file will be created and saved as `hi.wav`
`-p`<br>`--play` | Play a Morse Code audio file | At the prompt, enter *hi* and if `hi.wav` exists, the audio will be played
`-r`<br>`--read` | Decipher a Morse Code audio file | At the prompt, enter *hi* and if `hi.wav` exists, the text *Hello World* will be displayed 