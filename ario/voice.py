"""Wake-Word, Spracherkennung (lokal) und Sprachausgabe."""
import asyncio, os, tempfile, threading
import numpy as np

import config

RATE, FRAME = 16000, 1280
_models = {}
# Hauptschleife und Hintergrund-Wächter dürfen nicht gleichzeitig sprechen
_speak_lock = threading.Lock()


def _wake():
    if "wake" not in _models:
        import openwakeword
        from openwakeword.model import Model
        openwakeword.utils.download_models()
        _models["wake"] = Model(wakeword_models=[config.WAKEWORD], inference_framework="onnx")
    return _models["wake"]


def _stt():
    if "stt" not in _models:
        from faster_whisper import WhisperModel
        _models["stt"] = WhisperModel(config.STT_MODEL, device="cpu", compute_type="int8")
    return _models["stt"]


def wait_for_wakeword():
    import sounddevice as sd
    wake = _wake()
    with sd.InputStream(samplerate=RATE, channels=1, dtype="int16", blocksize=FRAME) as s:
        while True:
            frame, _ = s.read(FRAME)
            if max(wake.predict(frame.flatten()).values()) > config.WAKE_THRESHOLD:
                wake.reset()
                return


def record_until_silence(max_s=15, silence_s=1.2, threshold=500):
    import sounddevice as sd
    chunks, quiet = [], 0
    with sd.InputStream(samplerate=RATE, channels=1, dtype="int16", blocksize=FRAME) as s:
        for _ in range(int(max_s * RATE / FRAME)):
            frame, _ = s.read(FRAME)
            chunks.append(frame.flatten())
            quiet = quiet + 1 if np.abs(frame).mean() < threshold else 0
            if quiet * FRAME / RATE > silence_s and len(chunks) > 10:
                break
    return np.concatenate(chunks).astype(np.float32) / 32768


def transcribe(audio):
    segments, _ = _stt().transcribe(audio, language="de")
    return " ".join(s.text for s in segments).strip()


def speak(text):
    import edge_tts, pygame
    if not text:
        return
    with _speak_lock:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)
        try:
            asyncio.run(edge_tts.Communicate(text, config.VOICE, rate="+10%").save(path))
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.wait(50)
            pygame.mixer.music.unload()
        finally:
            os.remove(path)
