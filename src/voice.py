import speech_recognition as sr
import time

class Listener:
    def __init__(self, mic_index, lang_in_code, on_recognized, on_error, stop_event):
        self.mic_index = mic_index
        self.lang_in_code = lang_in_code
        self.on_recognized = on_recognized
        self.on_error = on_error
        self.stop_event = stop_event
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone(device_index=self.mic_index) as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            while not self.stop_event.is_set():
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio, language=self.lang_in_code)
                    self.on_recognized(text)
                except sr.WaitTimeoutError:
                    self.on_error("Nenhuma fala detectada, tentando novamente...")
                except sr.UnknownValueError:
                    self.on_error("Não entendi o que você falou.")
                except sr.RequestError as e:
                    self.on_error(f"Erro na requisição: {e}")
                    time.sleep(2)
