from PySide6.QtWidgets import (
    QTextEdit, QLineEdit, QPushButton, QHBoxLayout,
    QVBoxLayout, QWidget, QLabel, QComboBox
)
from PySide6.QtCore import Qt, Signal
from api.tts_client import TTSMode  # 导入枚举类

class ChatDisplay(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        font = self.font()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.setFont(font)

    def add_message(self, sender, message):
        self.append(f"{sender}: {message}\n")

class InputArea(QWidget):
    send_signal = Signal()
    set_audio_signal = Signal()
    exit_signal = Signal()
    tts_mode_changed = Signal(int)  # 新增TTS模式切换信号


    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 修改下拉框的添加方式，使用枚举值
        self.tts_mode_combo = QComboBox()
        self.tts_mode_combo.addItem("禁用语音", TTSMode.DISABLED.value)
        self.tts_mode_combo.addItem("Python TTS", TTSMode.PYTHON.value)
        self.tts_mode_combo.addItem("GPT-SoVits-TTS", TTSMode.CUSTOM.value)
        self.tts_mode_combo.currentIndexChanged.connect(
            lambda: self.tts_mode_changed.emit(self.tts_mode_combo.currentData())
        )

        layout.addWidget(QLabel("语音模式:"))
        layout.addWidget(self.tts_mode_combo)

        self.user_input = QLineEdit()

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("输入您的问题...")
        self.user_input.returnPressed.connect(self.emit_send_signal)
        font = self.user_input.font()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(12)
        self.user_input.setFont(font)
        layout.addWidget(self.user_input)

        send_button = QPushButton("发送")
        send_button.clicked.connect(self.emit_send_signal)
        layout.addWidget(send_button)

        ref_audio_button = QPushButton("设置参考音频")
        ref_audio_button.clicked.connect(self.set_audio_signal.emit)
        layout.addWidget(ref_audio_button)

        # 添加退出按钮
        exit_button = QPushButton("退出")
        exit_button.clicked.connect(self.exit_signal.emit)
        layout.addWidget(exit_button)

    def get_text(self):
        return self.user_input.text().strip()

    def clear(self):
        self.user_input.clear()

    def emit_send_signal(self):
        self.send_signal.emit()

class StatusBar(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignLeft)
        self.set_text("就绪")

    def set_text(self, text):
        self.setText(text)