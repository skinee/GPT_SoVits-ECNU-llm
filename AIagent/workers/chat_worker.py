from PySide6.QtCore import QObject, Signal

class OpenAIChatWorker(QObject):
    finished = Signal(str)  # 返回 AI 回复
    error_occurred = Signal(str)  # 返回错误信息

    def __init__(self, openai_client, user_input):
        super().__init__()
        self.openai_client = openai_client
        self.user_input = user_input

    def run(self):
        try:
            response_content = self.openai_client.get_response(self.user_input)
            self.finished.emit(response_content)
        except Exception as e:
            self.error_occurred.emit(str(e))