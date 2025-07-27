import tkinter as tk
from tkinter import ttk
import threading
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langdetect import detect
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os
import time
import math

# Load chatbot and translation models
chat_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
chat_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
en_to_ur = pipeline("translation_en_to_ur", model="Helsinki-NLP/opus-mt-en-ur")
ur_to_en = pipeline("translation_ur_to_en", model="Helsinki-NLP/opus-mt-ur-en")
recognizer = sr.Recognizer()

chat_history_ids = None
step_counter = 0


def speak(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"response_{int(time.time())}.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("🔇 Speech error:", e)


def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language='ur-PK')
        except:
            return None


def generate_response(prompt):
    global chat_history_ids, step_counter
    new_input_ids = chat_tokenizer.encode(prompt + chat_tokenizer.eos_token, return_tensors='pt')
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    chat_history_ids = chat_model.generate(
        bot_input_ids,
        max_length=1000,
        pad_token_id=chat_tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8
    )

    step_counter += 1
    if step_counter >= 6:
        chat_history_ids = None
        step_counter = 0

    return chat_tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


# --------------------- JARVIS-STYLE GUI ---------------------

class SANGICanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#000000', highlightthickness=0)
        self.animation_frame = 0
        self.listening = False
        self.pulse_radius = 80
        self.draw_interface()
        self.animate()
    
    def draw_interface(self):
        self.delete("all")
        width, height = 400, 400
        center_x, center_y = width // 2, height // 2
        
        # Outer rotating rings
        for i in range(5):
            radius = 150 - i * 15
            offset = (self.animation_frame + i * 20) % 360
            self.draw_rotating_ring(center_x, center_y, radius, offset, i)
        
        # Central core
        core_color = "#00ffff" if self.listening else "#0088ff"
        self.create_oval(center_x - 40, center_y - 40, center_x + 40, center_y + 40,
                        outline=core_color, width=3, fill="#001122")
        
        # Pulsing effect when listening
        if self.listening:
            pulse_intensity = abs(math.sin(self.animation_frame * 0.2))
            pulse_color = f"#{int(pulse_intensity * 255):02x}{int(pulse_intensity * 255):02x}ff"
            self.create_oval(center_x - self.pulse_radius, center_y - self.pulse_radius,
                           center_x + self.pulse_radius, center_y + self.pulse_radius,
                           outline=pulse_color, width=2)
        
        # SANGI text in center
        self.create_text(center_x, center_y, text="S.A.N.G.I", 
                        font=("Orbitron", 16, "bold"), fill="#00ffff")
        
        # Status indicators
        status_color = "#00ff00" if self.listening else "#ffaa00"
        for i in range(8):
            angle = i * 45
            x = center_x + 60 * math.cos(math.radians(angle + self.animation_frame))
            y = center_y + 60 * math.sin(math.radians(angle + self.animation_frame))
            self.create_oval(x-2, y-2, x+2, y+2, fill=status_color, outline="")
    
    def draw_rotating_ring(self, cx, cy, radius, offset, ring_index):
        points = 60
        colors = ["#004488", "#0066aa", "#0088cc", "#00aaee", "#00ccff"]
        color = colors[ring_index % len(colors)]
        
        for i in range(0, points, 2):
            angle1 = (i * 360 / points + offset) % 360
            angle2 = ((i + 1) * 360 / points + offset) % 360
            
            x1 = cx + radius * math.cos(math.radians(angle1))
            y1 = cy + radius * math.sin(math.radians(angle1))
            x2 = cx + radius * math.cos(math.radians(angle2))
            y2 = cy + radius * math.sin(math.radians(angle2))
            
            self.create_line(x1, y1, x2, y2, fill=color, width=2)
    
    def set_listening(self, listening):
        self.listening = listening
    
    def animate(self):
        self.animation_frame += 2
        self.draw_interface()
        self.after(50, self.animate)


class SANGIStyle:
    @staticmethod
    def configure_style():
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure('SANGI.TButton',
                       background='#001122',
                       foreground='#00ffff',
                       borderwidth=2,
                       focuscolor='#00ffff',
                       relief='flat')
        
        style.map('SANGI.TButton',
                 background=[('active', '#002244'),
                           ('pressed', '#003366')])


class SANGILogFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#000011')
        self.setup_log()
    
    def setup_log(self):
        # Create scrolled text widget with cyberpunk styling
        self.log_frame = tk.Frame(self, bg='#000011')
        self.log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(self.log_frame, 
                               height=12, 
                               bg='#000011', 
                               fg='#00ffaa',
                               font=('Consolas', 10),
                               wrap='word',
                               insertbackground='#00ffff',
                               selectbackground='#004444',
                               relief='flat',
                               borderwidth=2)
        
        self.scrollbar = tk.Scrollbar(self.log_frame, 
                                     bg='#001122',
                                     troughcolor='#000011',
                                     activebackground='#00ffff')
        
        self.log_text.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.log_text.yview)
        
        # Initial message
        self.add_message("SYSTEM", "S.A.N.G.I Voice Agent Initialized...", "#00ffff")
        self.add_message("STATUS", "Ready for voice commands", "#00ff00")
    
    def add_message(self, label, message, color="#00ffaa"):
        timestamp = time.strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {label}: {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert('end', formatted_msg)
        self.log_text.config(state='disabled')
        self.log_text.see('end')
        
        # Color coding for different message types
        if label == "SYSTEM":
            self.log_text.tag_add("system", f"end-{len(formatted_msg)}c", "end-1c")
            self.log_text.tag_config("system", foreground="#00ffff")
        elif label == "USER":
            self.log_text.tag_add("user", f"end-{len(formatted_msg)}c", "end-1c")
            self.log_text.tag_config("user", foreground="#ffff00")
        elif label == "SANGI":
            self.log_text.tag_add("sangi", f"end-{len(formatted_msg)}c", "end-1c")
            self.log_text.tag_config("sangi", foreground="#00ff88")


class SANGIMainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("S.A.N.G.I - Advanced Voice Agent")
        self.root.geometry("900x700")
        self.root.configure(bg='#000000')
        self.root.resizable(True, True)
        
        # Configure styles
        SANGIStyle.configure_style()
        
        self.setup_ui()
        self.listening_active = False
    
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#000000')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title section
        title_frame = tk.Frame(main_container, bg='#000000')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(title_frame, 
                              text="S.A.N.G.I", 
                              font=('Orbitron', 32, 'bold'),
                              fg='#00ffff',
                              bg='#000000')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Smart Autonomous Neural General Intelligence",
                                 font=('Arial', 12),
                                 fg='#0088ff',
                                 bg='#000000')
        subtitle_label.pack()
        
        # Main content area
        content_frame = tk.Frame(main_container, bg='#000000')
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - SANGI interface
        left_panel = tk.Frame(content_frame, bg='#000000')
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # SANGI canvas
        self.sangi_canvas = SANGICanvas(left_panel, width=400, height=400)
        self.sangi_canvas.pack(pady=10)
        
        # Control buttons
        button_frame = tk.Frame(left_panel, bg='#000000')
        button_frame.pack(pady=10)
        
        self.listen_button = ttk.Button(button_frame,
                                       text="🎤 ACTIVATE LISTENING",
                                       style='SANGI.TButton',
                                       command=self.toggle_listening)
        self.listen_button.pack(pady=5)
        
        self.status_label = tk.Label(button_frame,
                                    text="STATUS: STANDBY",
                                    font=('Consolas', 10, 'bold'),
                                    fg='#ffaa00',
                                    bg='#000000')
        self.status_label.pack(pady=5)
        
        # Right panel - Log area
        right_panel = tk.Frame(content_frame, bg='#000000')
        right_panel.pack(side='right', fill='both', expand=True)
        
        log_title = tk.Label(right_panel,
                            text="COMMUNICATION LOG",
                            font=('Orbitron', 14, 'bold'),
                            fg='#00ffff',
                            bg='#000000')
        log_title.pack(pady=(0, 10))
        
        self.log_frame = SANGILogFrame(right_panel)
        self.log_frame.pack(fill='both', expand=True)
    
    def toggle_listening(self):
        if not self.listening_active:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        self.listening_active = True
        self.sangi_canvas.set_listening(True)
        self.listen_button.config(text="⏹️ STOP LISTENING")
        self.status_label.config(text="STATUS: LISTENING", fg="#00ff00")
        self.log_frame.add_message("SYSTEM", "Voice recognition activated", "#00ff00")
        threading.Thread(target=self.listen_and_respond, daemon=True).start()
    
    def stop_listening(self):
        self.listening_active = False
        self.sangi_canvas.set_listening(False)
        self.listen_button.config(text="🎤 ACTIVATE LISTENING")
        self.status_label.config(text="STATUS: STANDBY", fg="#ffaa00")
        self.log_frame.add_message("SYSTEM", "Voice recognition deactivated", "#ffaa00")
    
    def listen_and_respond(self):
        if not self.listening_active:
            return
            
        user_input = listen()
        if not user_input:
            self.log_frame.add_message("ERROR", "Could not understand audio input", "#ff4444")
            self.stop_listening()
            return

        try:
            lang = detect(user_input)
            self.log_frame.add_message("USER", f"{user_input} (Lang: {lang})", "#ffff00")

            if lang == 'ur':
                translated = ur_to_en(user_input)[0]['translation_text']
                self.log_frame.add_message("TRANSLATE", f"EN: {translated}", "#88aaff")
            else:
                translated = user_input

            self.status_label.config(text="STATUS: PROCESSING", fg="#ff8800")
            bot_en = generate_response(translated)
            self.log_frame.add_message("SANGI", bot_en, "#00ff88")

            if lang == 'ur':
                try:
                    bot_ur = en_to_ur(bot_en)[0]['translation_text']
                    speak(bot_ur, lang='ur')
                    self.log_frame.add_message("SANGI", f"UR: {bot_ur}", "#00ff88")
                except:
                    speak(bot_en, lang='en')
                    self.log_frame.add_message("SYSTEM", "Translation failed, using English", "#ff8800")
            else:
                speak(bot_en, lang='en')
                
        except Exception as e:
            self.log_frame.add_message("ERROR", f"Processing error: {str(e)}", "#ff4444")
        
        self.stop_listening()


# --------------------- RUN SANGI ---------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SANGIMainUI(root)
    root.mainloop()
