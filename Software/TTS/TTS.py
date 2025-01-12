import pyttsx3

class TextToSpeech:
    def __init__(self, rate=150, volume=1, voice_type=0):
        """
        Initializes the TextToSpeech engine with the given configurations.
        :param rate: Rate of speech (default is 150 words per minute)
        :param volume: Volume of speech (default is 1, range is 0.0 to 1.0)
        :param voice_type: Type of voice (0 for Male, 1 for Female)
        """
        self.engine = pyttsx3.init()
        self.configure(rate, volume, voice_type)

    def configure(self, rate, volume, voice_type):
        """
        Configures the speech engine with the given rate, volume, and voice type.
        :param rate: Rate of speech (words per minute)
        :param volume: Volume of speech (range 0.0 to 1.0)
        :param voice_type: Type of voice (0 for Male, 1 for Female)
        """
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_type].id)

    def speak(self, text):
        """
        Speaks the given text out loud.
        :param text: The text to convert to speech
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def set_rate(self, rate):
        """
        Sets the speech rate.
        :param rate: Rate of speech (words per minute)
        """
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """
        Sets the speech volume.
        :param volume: Volume of speech (range 0.0 to 1.0)
        """
        self.engine.setProperty('volume', volume)

    def set_voice(self, voice_type):
        """
        Sets the voice type.
        :param voice_type: Type of voice (0 for Male, 1 for Female)
        """
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_type].id)
