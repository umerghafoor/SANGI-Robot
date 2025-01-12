import pyttsx3

# Initialize 
engine = pyttsx3.init()

def configuration(rate, volume, voice_type):
    """"
    rate = The rate of speech
    volume = The volume of speech
    voice = 0/1 for Male/Female

    """
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_type].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

while(1):
    # Input
    answer = input("Enter the input you want to convert to speech: ")

    # Configuration    
    configuration(100, 1, 0)

    # Output
    speak(answer)
