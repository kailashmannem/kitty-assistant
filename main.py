import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from kitty_window import KittyWindow
import kitty_genai

app = QApplication(sys.argv)

# Initialize Gemini API key and URL after QApplication is created
key = kitty_genai.get_gemini_api_key()
if not key:
    msg = QMessageBox()
    msg.setWindowTitle('Kitty Party denied!')
    msg.setText("Kitty no talk you, kitty angy! 😾")
    msg.setStyleSheet('''
        QMessageBox { background: #181a20; border-radius: 12px; }
        QLabel { color: #e6e6e6; font-size: 15px; }
        QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
        QPushButton:hover { background: #2563eb; }
    ''')
    msg.exec_()
    sys.exit(0)
kitty_genai.GEMINI_API_KEY = key
kitty_genai.GEMINI_API_URL = kitty_genai.get_gemini_api_url(key)

screen = app.primaryScreen()
kitty = KittyWindow()
kitty.show()

sys.exit(app.exec_())
