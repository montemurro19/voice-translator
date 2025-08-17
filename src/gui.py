import customtkinter as ctk
from .utils import listar_microfones_reais
from .voice import Listener
from .tts import Speaker
from googletrans import Translator
from threading import Thread, Event

class VoiceTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Translator")
        self.root.geometry("820x420")
        self.root.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Dicionário de idiomas
        self.lang_dict = {
            'Português': 'pt-BR',
            'Espanhol': 'es',
            'Inglês': 'en'
        }

        self.translator = Translator()
        self.speaker = Speaker()
        self.listener = None
        self.listening_thread = None
        self.stop_event = Event()

        self.status_var = ctk.StringVar(value="Aguardando...")
        self.mic_names = listar_microfones_reais()
        self.selected_mic = ctk.StringVar(value=self.mic_names[0] if self.mic_names else "")

        self.layout_ui()

    def layout_ui(self):
        # Frame principal centralizado
        main_frame = ctk.CTkFrame(self.root, corner_radius=16, fg_color="#313552")
        main_frame.pack(fill="both", padx=32, pady=32, expand=True)

        # Frame de configurações (esquerda) com tema escuro garantido
        config_frame = ctk.CTkFrame(main_frame,
                                    corner_radius=12,
                                    width=260,
                                    height=330,
                                    fg_color="#181926")  # cor bem escura
        config_frame.grid(row=0, column=0, rowspan=2, padx=(10, 30), pady=15, sticky="ns")

        # Título das configurações
        ctk.CTkLabel(config_frame, text="Configurações", font=("Arial", 18, "bold"),
                     text_color="#f2e9e4").pack(pady=(15, 5))

        # Microfone
        ctk.CTkLabel(config_frame, text="Microfone", font=("Arial", 14), text_color="#f2e9e4").pack(pady=(20, 3))
        self.combo_mic = ctk.CTkComboBox(config_frame, values=self.mic_names, variable=self.selected_mic, width=220)
        self.combo_mic.pack(pady=2, padx=12)  # margem lateral aqui!

        # Idioma de entrada
        ctk.CTkLabel(config_frame, text="Idioma de entrada", font=("Arial", 14), text_color="#f2e9e4").pack(pady=(18, 3))
        self.lang_in_var = ctk.StringVar(value='Português')
        self.combo_lang_in = ctk.CTkComboBox(config_frame, values=list(self.lang_dict.keys()), variable=self.lang_in_var, width=220)
        self.combo_lang_in.pack(pady=2, padx=12)  # margem lateral aqui!

        # Idioma de saída
        ctk.CTkLabel(config_frame, text="Idioma de saída", font=("Arial", 14), text_color="#f2e9e4").pack(pady=(18,3))
        self.lang_out_var = ctk.StringVar(value='Espanhol')
        self.combo_lang_out = ctk.CTkComboBox(config_frame, values=list(self.lang_dict.keys()), variable=self.lang_out_var, width=220)
        self.combo_lang_out.pack(pady=(2, 10), padx=12)  # margem lateral aqui!

        # Status box (centralizado, grande)
        self.status_label = ctk.CTkLabel(
            main_frame,
            textvariable=self.status_var,
            font=("Arial", 22, "bold"),
            anchor="center",
            width=350,
            height=180,
            fg_color="#4a4e69",
            corner_radius=12,
            text_color="#f2e9e4"
        )
        self.status_label.grid(row=0, column=1, pady=(30, 8), padx=(8, 15), sticky="nsew")

        # Frame botões (horizontal, central)
        button_frame = ctk.CTkFrame(main_frame, corner_radius=12, fg_color="#181926")  # tema escuro
        button_frame.grid(row=1, column=1, padx=8, pady=(8, 25), sticky="s")

        self.play_button = ctk.CTkButton(
            button_frame, text="Play", width=140,
            font=("Arial", 16, "bold"),
            command=self.start_listening,
            fg_color="#0099ff", hover_color="#58a4b0"
        )
        self.play_button.pack(side="left", padx=20, pady=15)

        self.stop_button = ctk.CTkButton(
            button_frame, text="Stop", width=140,
            font=("Arial", 16, "bold"),
            command=self.stop_listening,
            state="disabled",
            fg_color="#e63946", hover_color="#ff686b"
        )
        self.stop_button.pack(side="left", padx=20, pady=15)

        # Permitir que as colunas cresçam
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    # ------------------------------
    # Lógica
    # ------------------------------
    def start_listening(self):
        if self.listening_thread is None or not self.listening_thread.is_alive():
            self.stop_event.clear()
            self.listening_thread = Thread(target=self.listen_loop, daemon=True)
            self.listening_thread.start()
            self.status_var.set("🎙 Escutando...")
            self.play_button.configure(state="disabled")
            self.stop_button.configure(state="normal")

    def stop_listening(self):
        self.stop_event.set()
        self.status_var.set("⏹ Parado")
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

    def listen_loop(self):
        mic_index = self.mic_names.index(self.selected_mic.get())
        lang_in_code = self.lang_dict[self.lang_in_var.get()]
        lang_out_code = self.lang_dict[self.lang_out_var.get()]

        def on_recognized(text):
            self.status_var.set(f"🗣 Você disse: {text}")
            translated = self.translator.translate(text, src=lang_in_code[:2], dest=lang_out_code[:2])
            self.status_var.set(f"📌 Tradução: {translated.text}")
            self.speaker.speak(translated.text, lang_out_code)

        def on_error(msg):
            self.status_var.set(f"⚠ {msg}")
            self.speaker.speak(msg, lang_in_code)

        self.listener = Listener(
            mic_index=mic_index,
            lang_in_code=lang_in_code,
            on_recognized=on_recognized,
            on_error=on_error,
            stop_event=self.stop_event
        )
        self.listener.listen()

        # Reset
        self.status_var.set("⏹ Parado")
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

if __name__ == "__main__":
    app = ctk.CTk()
    VoiceTranslatorApp(app)
    app.mainloop()
