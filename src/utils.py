import speech_recognition as sr

def listar_microfones_reais():
    todos_dispositivos = sr.Microphone.list_microphone_names()
    vistos = set()
    microfones = []
    for nome in todos_dispositivos:
        if "microfone" in nome.lower() and nome not in vistos:
            vistos.add(nome)
            microfones.append(nome)
    return microfones
