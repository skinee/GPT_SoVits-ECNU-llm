import os
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from .widgets import ChatDisplay, InputArea, StatusBar
from api.openai_client import OpenAIClient
from api.tts_client import TTSClient
from workers.chat_worker import OpenAIChatWorker
from workers.tts_worker import TTSWorker
from PySide6.QtCore import QThread
from api.tts_client import TTSMode

class ChatbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AIagent")
        self.resize(800, 600)

        # 初始化客户端
        self.openai_client = OpenAIClient()
        self.tts_client = TTSClient()

        # 创建界面
        self.init_ui()

    def init_ui(self):
        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # 对话显示区域
        self.chat_display = ChatDisplay()
        layout.addWidget(self.chat_display)

        # 用户输入区域
        self.input_area = InputArea()
        self.input_area.send_signal.connect(self.send_message)
        self.input_area.exit_signal.connect(self.close)  # 连接退出信号
        layout.addWidget(self.input_area)

        # 状态栏
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)

        # 连接信号
        self.input_area.set_audio_signal.connect(self.set_reference_audio)

        # 连接退出信号
        self.input_area.exit_signal.connect(self.close)

        self.input_area.tts_mode_changed.connect(self.set_tts_mode)

    def set_tts_mode(self, mode):
        """设置TTS模式"""
        # 将数字转换为枚举值
        if isinstance(mode, int):
            mode = TTSMode(mode)
        self.tts_client.set_mode(mode)

        # 使用枚举值进行比较
        mode_desc = {
            TTSMode.DISABLED: "禁用语音",
            TTSMode.PYTHON: "Python TTS",
            TTSMode.CUSTOM: "GPT-SoVits-TTS"
        }.get(mode, "未知模式")

        self.status_bar.set_text(f"已切换至 {mode_desc} 模式")

    def set_reference_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择参考音频文件",
            "",
            "WAV 文件 (*.wav)"
        )
        if file_path:
            self.tts_client.set_reference_audio(file_path)
            self.status_bar.set_text(f"参考音频已设置为: {file_path}")

    def send_message(self):
        user_input = self.input_area.get_text()
        if not user_input:
            return

        self.input_area.clear()
        self.chat_display.add_message("您", user_input)
        self.status_bar.set_text("正在处理请求...")

        # 启动 OpenAI 请求线程
        self.openai_thread = QThread()
        self.openai_worker = OpenAIChatWorker(self.openai_client, user_input)
        self.openai_worker.moveToThread(self.openai_thread)

        self.openai_thread.started.connect(self.openai_worker.run)
        self.openai_worker.finished.connect(self.handle_openai_response)
        self.openai_worker.error_occurred.connect(self.handle_error)
        self.openai_worker.finished.connect(self.openai_thread.quit)
        self.openai_worker.error_occurred.connect(self.openai_thread.quit)

        self.openai_thread.start()

    def handle_openai_response(self, response_content):
        self.chat_display.add_message("助手", response_content)

        if self.tts_client.mode == TTSMode.DISABLED:
            self.status_bar.set_text("就绪 (语音已禁用)")
            return

        # 使用枚举值获取模式描述
        mode_desc = {
            TTSMode.PYTHON: "Python TTS",
            TTSMode.CUSTOM: "GPT-SoVits-TTS"
        }.get(self.tts_client.mode, "未知模式")

        self.status_bar.set_text(f"正在使用{mode_desc}合成语音...(如若使用GPT-SoVits-TTS，请等待30s的合成，超时会自动取消)")

        # 启动TTS线程
        self.tts_thread = QThread()
        self.tts_worker = TTSWorker(self.tts_client, response_content)
        self.tts_worker.moveToThread(self.tts_thread)

        self.tts_thread.started.connect(self.tts_worker.run)
        self.tts_worker.finished.connect(self._handle_tts_result)
        self.tts_worker.error_occurred.connect(self.handle_error)
        self.tts_worker.finished.connect(self.tts_thread.quit)
        self.tts_worker.error_occurred.connect(self.tts_thread.quit)

        self.tts_thread.start()

    def _handle_tts_result(self, success):
        """处理TTS完成结果"""
        if success:
            self.status_bar.set_text("就绪")
        else:
            self.status_bar.set_text("语音合成失败")

    def handle_tts_finished(self):
        self.status_bar.set_text("就绪")

    def handle_error(self, error_msg):
        self.chat_display.add_message("系统", f"发生错误：{error_msg}")
        self.status_bar.set_text("错误发生")
        QMessageBox.critical(self, "错误", f"发生错误：{error_msg}")

    def closeEvent(self, event):
        # 清理临时文件
        if os.path.exists('temp.wav'):
            os.remove('temp.wav')
        event.accept()