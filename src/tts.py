from gtts import gTTS
import pygame
import tempfile
import os
import time

class Speaker:
    def __init__(self):
        pygame.mixer.init()

    def speak(self, text, lang_code):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            filename = fp.name
        try:
            tts = gTTS(text=text, lang=lang_code)
            tts.save(filename)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        finally:
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {e}")
