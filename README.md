# Voice Translator

Aplicação de tradução por voz com interface gráfica em Tkinter, reconhecimento de fala, tradução automática e síntese de voz (TTS). Fale em um idioma, veja a tradução e ouça o áudio traduzido.

---

## Funcionalidades

- Seleção de microfone disponível.
- Escolha do idioma de entrada e de saída (Português, Espanhol, Inglês).
- Tradução automática da fala.
- Reprodução do texto traduzido em áudio.

---

## Pré-requisitos

- **Python 3.8+**
- Microfone instalado e configurado no sistema.
- Conexão de internet (para reconhecimento de fala, tradução e TTS).

---

## Instalação

1. **Clone este repositório:**
    ```
    git clone https://github.com/seuusuario/voice_translator.git
    cd voice_translator
    ```

2. **(Opcional) Crie um ambiente virtual:**
    ```
    python -m venv venv
    source venv/bin/activate       # Linux/macOS
    venv\Scripts\activate          # Windows
    ```

3. **Instale as dependências:**
    ```
    pip install -r requirements.txt
    ```

---

## Como executar


Execute o comando abaixo na raiz do projeto:

python -m src.main

---

## Como usar

1. Abra a aplicação.
2. Selecione o microfone desejado.
3. Escolha o idioma de entrada e de saída.
4. Clique em **Play** para começar a gravar sua fala.
5. Aguarde a tradução e reprodução em áudio.
6. Clique em **Stop** para encerrar a escuta.

---

## Problemas frequentes

- Se não encontrar microfones, verifique se o dispositivo está ativo no seu sistema operacional.
- Todos recursos de voz e tradução usam serviços web (Google). Quedas ou limitações podem gerar erros temporários.
- Algumas dependências podem dar warning em Windows. Use sempre Python atualizado.
- No Linux/macOS, instale pacotes como `portaudio` ou equivalentes caso encontre erro com `speech_recognition`.

---

## Licença

Uso livre para fins de aprendizagem, estudo e aprimoramento.
