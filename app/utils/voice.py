from gtts import gTTS
import os
import tempfile

def speak_malayalam(text, lang='ml'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        tts.save(temp_path)
    return temp_path
