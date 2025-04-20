from PySide6.QtCore import QObject, Signal

class TTSWorker(QObject):
    finished = Signal(bool)  # 改为返回成功状态
    error_occurred = Signal(str)

    def __init__(self, tts_client, text):
        super().__init__()
        self.tts_client = tts_client
        self.text = text

    def run(self):
        try:
            success = self.tts_client.synthesize_speech(self.text)
            self.finished.emit(success)
        except Exception as e:
            self.error_occurred.emit(f"语音合成失败: {str(e)}")
            self.finished.emit(False)