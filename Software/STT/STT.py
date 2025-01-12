import speech_recognition as sr

def wait_for_activation(recognizer):
    """Wait for the user to say 'Hey SANGI' to activate the system."""
    with sr.Microphone() as source:
        print("Waiting for the activation phrase: 'Hey SANGI'...")
        try:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Listen for input
            audio_data = recognizer.listen(source)
            command = recognizer.recognize_google(audio_data)
            
            # Check for the activation phrase
            if command.lower() == "hey sangi":
                print("Activation phrase detected. The system is now active!")
                return True
            else:
                print(f"You said: '{command}', which is not the activation phrase.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
    return False

def speech_to_text():
    """Continuously listen to the user until they say 'Deactivate'."""
    recognizer = sr.Recognizer()

    # Wait for the activation phrase
    while not wait_for_activation(recognizer):
        pass

    print("The system is active. Say 'Deactivate' to stop.")
    while True:
        with sr.Microphone() as source:
            print("\nListening... Speak something!")
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = recognizer.listen(source)
                print("Processing...")
                text = recognizer.recognize_google(audio_data)
                print("You said:", text)

                # Check for the stop command
                if text.lower() == "deactivate":
                    print("Deactivating system. Goodbye!")
                    break
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")

# Run the speech-to-text function
if __name__ == "__main__":
    speech_to_text()
