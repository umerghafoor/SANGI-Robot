import speech_recognition as sr
import difflib
import time

class SpeechRecognizer:
    def __init__(self, inactivity_timeout=5, silence_duration=3.0):
        """Initialize the Speech Recognizer."""
        self.recognizer = sr.Recognizer()
        self.inactivity_timeout = inactivity_timeout
        self.silence_duration = silence_duration  # Duration to wait before considering speech as finished

    def wait_for_activation(self, activation_phrase="sangeet", similarity_threshold=0.8):
        """Wait for the activation phrase to activate the system with some tolerance for slight errors."""
        with sr.Microphone() as source:
            print(f"Waiting for the activation phrase: '{activation_phrase}'...")
            while True:
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio_data = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio_data)
                    print(f"You said: '{command}'")

                    for phrase in command.split(" "):
                        similarity = difflib.SequenceMatcher(None, phrase.lower(), activation_phrase.lower()).ratio()
                        print(f"Similarity: {similarity:.2f}")

                        if similarity >= similarity_threshold:
                            print(f"Activation phrase detected with similarity: {similarity:.2f}. The system is now active!")
                            return True
                        else:
                            print(f"Command '{command}' did not match the activation phrase.")
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand that.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")

    def speech_to_text(self):
        """Listen continuously and return the recognized speech as text."""
        with sr.Microphone() as source:
            print("\nListening... Speak something!")
            last_spoken_time = time.time()

            while True:
                try:
                    # Adjusting for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio_data = self.recognizer.listen(source, timeout=None, phrase_time_limit=None)  # Listen until silence
                    print("Processing...")
                    text = self.recognizer.recognize_google(audio_data)
                    print("You said:", text)
                    last_spoken_time = time.time()  # Reset time on every recognized phrase

                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand that.")
                except sr.RequestError as e:
                    print(f"Error with the speech recognition service: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

                # If there is no speech detected for the defined silence duration, process it
                if time.time() - last_spoken_time > self.silence_duration:
                    print("Detected a pause in speech. Processing input...")
                    yield text

                # Timeout only if the user has stopped speaking for a set period
                if time.time() - last_spoken_time > self.inactivity_timeout:
                    print(f"No speech detected for {self.inactivity_timeout} seconds. Going into disabled mode.")
                    break
