import os
import requests
import sounddevice as sd
import soundfile as sf
import pyttsx3
from enum import Enum, auto

class TTSMode(Enum):
    DISABLED = auto()
    PYTHON = auto()
    CUSTOM = auto()


class TTSClient:
    def __init__(self):
        # 默认模式
        self.mode = TTSMode.DISABLED
        # 自定义TTS配置
        self.custom_tts_url = "http://127.0.0.1:9880/"
        self.refer_wav_path = r"C:\Users\37535\Downloads\总不会连这点要求也满足不了吧，芙宁娜小姐？.wav"
        self.prompt_text = "总不会连这点要求也满足不了吧，芙宁娜小姐？"

        # Python TTS引擎
        self.py_engine = pyttsx3.init()
        voices = self.py_engine.getProperty('voices')
        if len(voices) > 0:
            self.py_engine.setProperty('voice', voices[0].id)  # 设置第一个可用语音



    def set_mode(self, mode):
        """设置TTS模式"""
        if isinstance(mode, int):
            mode = TTSMode(mode)
        self.mode = mode

    def synthesize_speech(self, text):
        if self.mode == TTSMode.DISABLED:
            return False

        try:
            if self.mode == TTSMode.PYTHON:
                self._use_python_tts(text)
            elif self.mode == TTSMode.CUSTOM:
                self._use_custom_tts(text)
            return True
        except Exception as e:
            print(f"TTS Error: {str(e)}")
            return False

    def _use_python_tts(self, text):
        """使用Python内置TTS"""
        self.py_engine.say(text)
        self.py_engine.runAndWait()

    def _use_custom_tts(self, text):
        """使用自定义TTS服务"""
        params = {
            "refer_wav_path": self.refer_wav_path,
            "prompt_text": self.prompt_text,
            "prompt_language": "zh",
            "text": text,
            "text_language": "zh"
        }
        response = requests.get(self.custom_tts_url, params=params, timeout=30)
        response.raise_for_status()

        # 临时文件处理
        temp_file = 'tts_temp.wav'
        try:
            with open(temp_file, 'wb') as f:
                f.write(response.content)

            data, samplerate = sf.read(temp_file)
            sd.play(data, samplerate)
            sd.wait()
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)