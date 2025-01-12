# STT
# Speech to Text Converter

This Python program uses the `speech_recognition` library to convert speech into text. The program listens continuously to the user's input through a microphone and keeps running until the user says "Deactivate," at which point it terminates gracefully.

## Features
- Continuously listens to the user's speech.
- Converts speech to text using Google's Speech Recognition API.
- Stops listening when the user says "Deactivate."

## How It Works
1. The program initializes the microphone and adjusts for ambient noise to improve accuracy.
2. It listens to the user's speech and converts it into text in real-time.
3. If the user says "Deactivate," the program stops listening and exits.

## Requirements
- Python 3.6 or higher
- The following Python libraries:
  - `speech_recognition`
  - `pyaudio`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/speech-to-text-converter.git


2. Navigate to the project directory
```bash
cd speech-to-text-converter
```

3. Install the required Python Libraries
```bash
pip install SpeechRecognition pyaudio
```

## Example Output
The system is active. Say 'Deactivate' to stop.

Listening... Speak something!
Processing...
You said: Hello robot

Listening... Speak something!
Processing...
You said: How are you?

Listening... Speak something!
Processing...
You said: Deactivate
Deactivating system. Goodbye!


