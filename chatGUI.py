import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Slot
import creds
import openAI
import speechToText as stt


conversation_history = ""
response = ""
c_h = ""

class ChatWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(creds.ASSISTANT_NAME + " (" + creds.GPT_MODEL + ")")
        self.setGeometry(100, 100, 500, 400)

        # Set up the layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.layout.addWidget(self.chat_display)

        # Input field
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message here...")
        self.chat_input.returnPressed.connect(self.send_message)
        self.layout.addWidget(self.chat_input)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.central_widget.setLayout(self.layout)


    @Slot()
    def send_message(self):

        message = self.chat_input.text()
        if message:
            # self.chat_display.append(f"You: {message}\n")
            self.add_user_message(message)
            self.chat_input.clear()
        self.send_message_to_gpt(message)

    def send_message_to_gpt(self, message):
        
        global conversation_history

        response, c_h = stt.handle_input(message, conversation_history)
        conversation_history += c_h
        self.chat_display.append(f"\n{creds.ASSISTANT_NAME}: {response}\n")

    def add_user_message(self, message):
        self.chat_display.append(
            f'''
            <div style="background-color: transparent; color: lightblue; clear: both;">
                <span style="padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%;">
                    You: {message}
                </span>
            </div>
            '''
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
