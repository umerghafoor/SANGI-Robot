import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import speech_recognition as sr
from langdetect import detect
from gtts import gTTS
import os
import tempfile
import pygame
import time

# Modern color palette
BG_COLOR = '#23272f'
ACCENT_COLOR = '#4fd1c5'
SANGI_COLOR = '#2d3748'
USER_COLOR = '#4a5568'
TEXT_COLOR = '#f7fafc'
BUTTON_COLOR = '#38b2ac'
BUTTON_HOVER = '#319795'
MATRIX_BG = '#1a202c'
MATRIX_BORDER = '#4fd1c5'

FONT = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")

# To use GPT4All, install with: pip install gpt4all
# The first run will prompt you to download a model (e.g., gpt4all-j)
from gpt4all import GPT4All

class SangiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SANGI - Sentient Desktop Assistant")
        self.geometry("480x820")
        self.minsize(440, 700)
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)
        self.iconify()
        self.deiconify()

        # Main container frame with grid layout
        main_frame = tk.Frame(self, bg=BG_COLOR)
        main_frame.pack(fill='both', expand=True)
        main_frame.grid_rowconfigure(3, weight=1)  # Make chat area expandable
        main_frame.grid_columnconfigure(0, weight=1)

        # Status label
        self.status_var = tk.StringVar(value="Status: Idle")
        status_label = tk.Label(main_frame, textvariable=self.status_var, font=FONT_BOLD, fg=ACCENT_COLOR, bg=BG_COLOR)
        status_label.grid(row=0, column=0, pady=(18, 8), sticky='n')

        # LED Matrix Frame
        matrix_frame = tk.Frame(main_frame, bg=BG_COLOR, highlightbackground=MATRIX_BORDER, highlightthickness=3, bd=0)
        matrix_frame.grid(row=1, column=0, pady=(0, 18), sticky='n')
        self.led_matrix = tk.Canvas(matrix_frame, width=288, height=288, bg=MATRIX_BG, bd=0, highlightthickness=0)
        self.led_matrix.pack()
        self.draw_led_matrix_placeholder()

        # Buttons Frame
        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.grid(row=2, column=0, pady=(0, 18), sticky='n')
        self.monitor_btn = self.create_modern_button(btn_frame, "Start Monitoring", self.start_monitoring)
        self.monitor_btn.grid(row=0, column=0, padx=8)
        self.happy_btn = self.create_modern_button(btn_frame, "Show Happy Face", self.show_happy_face)
        self.happy_btn.grid(row=0, column=1, padx=8)
        self.listen_btn = self.create_modern_button(btn_frame, "Start Listening", self.start_listening_thread)
        self.listen_btn.grid(row=0, column=2, padx=8)

        # Conversation area with chat bubbles
        chat_frame = tk.Frame(main_frame, bg=BG_COLOR)
        chat_frame.grid(row=3, column=0, sticky='nsew', padx=0, pady=(0, 10))
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)
        self.conversation = scrolledtext.ScrolledText(chat_frame, width=48, height=16, state='disabled', font=FONT, bg=SANGI_COLOR, fg=TEXT_COLOR, bd=0, wrap='word', relief='flat', padx=12, pady=12)
        self.conversation.grid(row=0, column=0, sticky='nsew')

        # Initialize pygame mixer
        pygame.mixer.init()
        self.is_animating = False

    def create_modern_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, font=FONT_BOLD, fg=TEXT_COLOR, bg=BUTTON_COLOR, activebackground=BUTTON_HOVER, activeforeground=TEXT_COLOR, bd=0, padx=18, pady=8, relief='flat', cursor='hand2', command=command)
        btn.bind("<Enter>", lambda e: btn.config(bg=BUTTON_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=BUTTON_COLOR))
        btn.configure(highlightthickness=0)
        return btn

    def draw_led_matrix_placeholder(self, face=None):
        self.led_matrix.delete("all")
        size = 16
        cell = 18
        for i in range(size):
            for j in range(size):
                self.led_matrix.create_rectangle(
                    j*cell, i*cell, (j+1)*cell, (i+1)*cell,
                    outline="#222", fill=MATRIX_BG
                )
        if face == 'happy':
            # Eyes
            self.led_matrix.create_rectangle(4*cell, 5*cell, 6*cell, 7*cell, fill=ACCENT_COLOR, outline="")
            self.led_matrix.create_rectangle(10*cell, 5*cell, 12*cell, 7*cell, fill=ACCENT_COLOR, outline="")
            # Smile
            for x in range(5, 11):
                self.led_matrix.create_rectangle(x*cell, 11*cell, (x+1)*cell, 13*cell, fill=ACCENT_COLOR, outline="")
        elif face == 'listening':
            # Animated listening face (ears up)
            self.led_matrix.create_rectangle(2*cell, 2*cell, 4*cell, 4*cell, fill=ACCENT_COLOR, outline="")
            self.led_matrix.create_rectangle(12*cell, 2*cell, 14*cell, 4*cell, fill=ACCENT_COLOR, outline="")
            self.led_matrix.create_rectangle(4*cell, 5*cell, 6*cell, 7*cell, fill=ACCENT_COLOR, outline="")
            self.led_matrix.create_rectangle(10*cell, 5*cell, 12*cell, 7*cell, fill=ACCENT_COLOR, outline="")
            for x in range(5, 11):
                self.led_matrix.create_rectangle(x*cell, 11*cell, (x+1)*cell, 13*cell, fill=ACCENT_COLOR, outline="")

    def animate_listening(self):
        self.is_animating = True
        for _ in range(4):
            if not self.is_animating:
                break
            self.draw_led_matrix_placeholder('listening')
            self.update()
            time.sleep(0.18)
            self.draw_led_matrix_placeholder('happy')
            self.update()
            time.sleep(0.18)
        self.draw_led_matrix_placeholder('happy')
        self.is_animating = False

    def start_monitoring(self):
        self.status_var.set("Status: Monitoring (simulated)")
        messagebox.showinfo("Monitoring", "Screen monitoring started (simulated)")

    def show_happy_face(self):
        self.status_var.set("Status: Showing Happy Face")
        self.draw_led_matrix_placeholder('happy')

    def start_listening_thread(self):
        threading.Thread(target=self.start_listening, daemon=True).start()

    def start_listening(self):
        self.status_var.set("Status: Listening...")
        self.append_conversation("SANGI", "Listening for your command...", sender='sangi')
        threading.Thread(target=self.animate_listening, daemon=True).start()
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                self.is_animating = False
                self.status_var.set("Status: Processing...")
                text = recognizer.recognize_google(audio, language="ur-PK,en-US")
                self.append_conversation("You", text, sender='user')
                lang = detect(text)
                response = self.generate_response(text, lang)
                self.append_conversation("SANGI", response, sender='sangi')
                self.speak(response, lang)
                self.status_var.set("Status: Idle")
                self.draw_led_matrix_placeholder('happy')
            except sr.WaitTimeoutError:
                self.is_animating = False
                self.status_var.set("Status: Idle")
                self.append_conversation("SANGI", "No speech detected.", sender='sangi')
                self.draw_led_matrix_placeholder('happy')
            except sr.UnknownValueError:
                self.is_animating = False
                self.status_var.set("Status: Idle")
                self.append_conversation("SANGI", "Sorry, I could not understand.", sender='sangi')
                self.draw_led_matrix_placeholder('happy')
            except Exception as e:
                self.is_animating = False
                self.status_var.set("Status: Idle")
                self.append_conversation("SANGI", f"Error: {str(e)}", sender='sangi')
                self.draw_led_matrix_placeholder('happy')

    def generate_response(self, text, lang):
        # Use GPT4All for real-time responses
        try:
            # Load the model from the user's specified path
            model = GPT4All("C:/Users/DELL/AppData/Local/nomic.ai/GPT4All/Meta-Llama-3-8B-Instruct.Q4_0.gguf")
            prompt = text
            if lang == 'ur':
                # Try to get a response in Urdu, but fallback if not possible
                prompt = f"Respond in Urdu: {text}"
            response = model.generate(prompt, max_tokens=128)
            # If Urdu, check if response is in Urdu, else fallback
            if lang == 'ur' and not any('\u0600' <= c <= '\u06FF' for c in response):
                return "(Urdu support is limited in this model.)\n" + response
            return response.strip()
        except Exception as e:
            return f"[GPT4All Error] {str(e)}"

    def speak(self, text, lang):
        try:
            tts_lang = 'en' if lang == 'en' else 'ur'
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_path = fp.name
            tts = gTTS(text=text, lang=tts_lang)
            tts.save(temp_path)
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                self.update()
            try:
                pygame.mixer.music.unload()
            except Exception:
                pass
            for _ in range(5):
                try:
                    os.remove(temp_path)
                    break
                except PermissionError:
                    time.sleep(0.2)
        except Exception as e:
            self.append_conversation("SANGI", f"TTS Error: {str(e)}", sender='sangi')

    def append_conversation(self, speaker, message, sender='sangi'):
        self.conversation.config(state='normal')
        if sender == 'user':
            bubble = f"\n  {speaker}: {message}"
            self.conversation.insert(tk.END, bubble + "\n", 'user')
        else:
            bubble = f"\n{speaker}: {message}"
            self.conversation.insert(tk.END, bubble + "\n", 'sangi')
        self.conversation.tag_config('user', background=USER_COLOR, foreground=TEXT_COLOR, lmargin1=30, lmargin2=30, rmargin=8, spacing3=4, font=FONT_BOLD)
        self.conversation.tag_config('sangi', background=SANGI_COLOR, foreground=ACCENT_COLOR, lmargin1=8, lmargin2=8, rmargin=30, spacing3=4, font=FONT)
        self.conversation.see(tk.END)
        self.conversation.config(state='disabled')

if __name__ == "__main__":
    app = SangiApp()
    app.mainloop() 