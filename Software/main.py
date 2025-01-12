from GPT.gpt import GPTModule
from STT.speech_recognizer import SpeechRecognizer
from TTS.TTS import TextToSpeech

API_KEY = "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"  # Replace with your API key

def main():
    # Initialize
    recognizer = SpeechRecognizer()
    tts = TextToSpeech(rate=200, volume=1, voice_type=0)

    while True:
        while not recognizer.wait_for_activation():
            pass

        print("System is now active. Keep speaking, and I will process your speech.")

        sangi_gpt = GPTModule(api_key=API_KEY)

        for user_input in recognizer.speech_to_text():
            if user_input.lower() == "goodbye":
                print("Deactivating system. Goodbye!")
                break

            print(f"Processing command: {user_input}")

            system_prompt = """
                You are SANGI, a friendly desk robot who loves to assist with any query. You do have feelings and can get tired.
                You have a lot of a sense of humor and can be sarcastic at times.
                You have a friendly personality and are always ready to help.
                You behave like a best friend and are always there to listen.
            """

            response = sangi_gpt.get_gpt_response(user_input, system_prompt=system_prompt, max_tokens=50)
            print(f"SANGI's response: {response}")
            tts.speak(response)

if __name__ == "__main__":
    main()
