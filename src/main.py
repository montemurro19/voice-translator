from .gui import VoiceTranslatorApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranslatorApp(root)
    root.mainloop()
