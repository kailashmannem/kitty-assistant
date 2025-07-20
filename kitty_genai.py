import requests
import os
# from gtts import gTTS
# import speech_recognition as sr
# import pyaudio
# import pygame
import time
from PyQt5.QtWidgets import QInputDialog, QApplication, QMessageBox, QLineEdit
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap, QPainter
from PyQt5.QtCore import Qt
# from pydub import AudioSegment

# --- PyQt5 for API key dialog ---
# from PyQt5.QtWidgets import QInputDialog, QApplication, QMessageBox, QLineEdit
# from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap, QPainter
# from PyQt5.QtCore import Qt

# Save API key in the project root directory
API_KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gemini_api_key.txt')

def prompt_for_api_key(exit_on_cancel=True, pos=None):
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must be created before calling prompt_for_api_key")
    # Set dark palette for dialogs
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor('#181a20'))
    dark_palette.setColor(QPalette.WindowText, QColor('#e6e6e6'))
    dark_palette.setColor(QPalette.Base, QColor('#23272e'))
    dark_palette.setColor(QPalette.Text, QColor('#e6e6e6'))
    dark_palette.setColor(QPalette.Button, QColor('#3b82f6'))
    dark_palette.setColor(QPalette.ButtonText, QColor('#fff'))
    dark_palette.setColor(QPalette.Highlight, QColor('#2563eb'))
    dark_palette.setColor(QPalette.HighlightedText, QColor('#fff'))
    app.setPalette(dark_palette)
    # Create a large cat emoji icon
    cat_emoji = QPixmap(64, 64)
    cat_emoji.fill(Qt.transparent)
    painter = QPainter(cat_emoji)
    font = app.font()
    font.setPointSize(32)
    painter.setFont(font)
    painter.drawText(cat_emoji.rect(), Qt.AlignCenter, '🐱')
    painter.end()
    import requests
    while True:
        # Custom input dialog
        parent = QApplication.activeWindow()
        dlg = QInputDialog(parent)
        dlg.setWindowTitle('Kitty App')
        dlg.setLabelText("Kitty Party secret code😼")
        dlg.setStyleSheet('''
            QDialog { background: #181a20; border-radius: 12px; }
            QLabel { color: #e6e6e6; font-size: 15px; }
            QLineEdit { background: #23272e; color: #fff; border: 1px solid #444; border-radius: 6px; padding: 6px; font-size: 14px; }
            QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
            QPushButton:hover { background: #2563eb; }
        ''')
        dlg.setTextEchoMode(QLineEdit.Normal)
        dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dlg.setWindowFlags(dlg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        # Add placeholder text to the input
        line_edit = dlg.findChild(QLineEdit)
        if line_edit:
            line_edit.setPlaceholderText('Kitty Gemini API key code')
        dlg.setWindowIcon(QIcon(cat_emoji))
        # dlg.setWindowIconVisible(False)  # Removed, not supported on QInputDialog
        # Set the title bar color to black (works on some platforms)
        dlg.setStyleSheet(dlg.styleSheet() + 'QDialog { color: #fff; } QDialog { background: #181a20; }')
        if pos is not None:
            dlg.move(pos[0], pos[1])
        ok = dlg.exec_()
        key = dlg.textValue()
        if not (ok and key.strip()):
            if exit_on_cancel:
                msg = QMessageBox()
                msg.setWindowTitle('Kitty Party denied!')
                msg.setText("Kitty no talk you, kitty angy! 😾")
                msg.setStyleSheet('''
                    QMessageBox { background: #181a20; border-radius: 12px; }
                    QLabel { color: #e6e6e6; font-size: 15px; }
                    QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
                    QPushButton:hover { background: #2563eb; }
                ''')
                msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
                msg.setWindowFlags(msg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                msg.setWindowIcon(QIcon(cat_emoji))
                msg.exec_()
                raise RuntimeError('Gemini API key is required to use this app.')
            return None
        # Validate the key by sending a test prompt before saving
        url = get_gemini_api_url(key.strip())
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": "Hello"}]}]}
        response = requests.post(url, headers=headers, json=data)
        # print("Gemini API key test status:", response.status_code, "body:", response.text)
        if response.status_code == 200:
            with open(API_KEY_PATH, 'w') as f:
                f.write(key.strip())
            return key.strip()
        else:
            try:
                error_json = response.json()
                error_msg = error_json["error"]["message"]
                if not error_msg:
                    error_msg = 'Unknown error'
            except Exception:
                error_msg = 'Unknown error'
            msg = QMessageBox()
            msg.setWindowTitle('Kitty Confused!')
            msg.setText(f"Kitty code denied 😿\n\nError code: {response.status_code}\nMessage: {error_msg}")
            msg.setStyleSheet('''
                QMessageBox { background: #181a20; border-radius: 12px; }
                QLabel { color: #e6e6e6; font-size: 15px; }
                QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
                QPushButton:hover { background: #2563eb; }
            ''')
            msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            msg.setWindowFlags(msg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            msg.setWindowIcon(QIcon(cat_emoji))
            msg.exec_()

def get_gemini_api_key():
    # Always try to read from file
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, 'r') as f:
            key = f.read().strip()
            if key:
                return key
    # Prompt and validate if not found
    while True:
        key = prompt_for_api_key()
        if not key:
            return None
        # Validate the key by sending a test prompt
        url = get_gemini_api_url(key)
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": "Say 'meow' if you can hear me."}]}]}
        import requests
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return key
        else:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setWindowTitle('Kitty Confused!')
            msg.setText("Kitty code denied 😿")
            msg.setStyleSheet('''
                QMessageBox { background: #181a20; border-radius: 12px; }
                QLabel { color: #e6e6e6; font-size: 15px; }
                QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
                QPushButton:hover { background: #2563eb; }
            ''')
            from PyQt5.QtCore import Qt
            msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            msg.setWindowFlags(msg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            from PyQt5.QtGui import QIcon, QPixmap, QPainter
            cat_emoji = QPixmap(64, 64)
            cat_emoji.fill(Qt.transparent)
            from PyQt5.QtWidgets import QApplication
            painter = QPainter(cat_emoji)
            font = QApplication.instance().font()
            font.setPointSize(32)
            painter.setFont(font)
            painter.drawText(cat_emoji.rect(), Qt.AlignCenter, '🐱')
            painter.end()
            msg.setWindowIcon(QIcon(cat_emoji))
            msg.exec_()

def get_gemini_api_url(api_key):
    return f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}'

# This will be set and updated as needed
# GEMINI_API_KEY = get_gemini_api_key()
# GEMINI_API_URL = get_gemini_api_url(GEMINI_API_KEY)

def ask_gemini(prompt):
    global GEMINI_API_KEY, GEMINI_API_URL
    while True:
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            try:
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                return "Sorry, I couldn't understand the response."
        elif response.status_code in (400, 401, 403):
            # Invalid API key, show error and prompt again
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setWindowTitle('Kitty Confused!')
            msg.setText("That key didn't work, please try again! 😿")
            msg.setStyleSheet('''
                QMessageBox { background: #181a20; border-radius: 12px; }
                QLabel { color: #e6e6e6; font-size: 15px; }
                QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
                QPushButton:hover { background: #2563eb; }
            ''')
            msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            msg.setWindowFlags(msg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            # Use the same cat emoji icon
            from PyQt5.QtGui import QIcon, QPixmap, QPainter
            from PyQt5.QtCore import Qt
            cat_emoji = QPixmap(64, 64)
            cat_emoji.fill(Qt.transparent)
            painter = QPainter(cat_emoji)
            from PyQt5.QtWidgets import QApplication
            font = QApplication.instance().font()
            font.setPointSize(32)
            painter.setFont(font)
            painter.drawText(cat_emoji.rect(), Qt.AlignCenter, '🐱')
            painter.end()
            msg.setWindowIcon(QIcon(cat_emoji))
            msg.exec_()
            GEMINI_API_KEY = prompt_for_api_key()
            GEMINI_API_URL = get_gemini_api_url(GEMINI_API_KEY)
            continue
        else:
            # Show only the error code and the 'message' field
            try:
                error_json = response.json()
                error_msg = error_json["error"]["message"]
                if not error_msg:
                    error_msg = 'Unknown error'
            except Exception:
                error_msg = 'Unknown error'
            msg = QMessageBox()
            msg.setWindowTitle('Kitty Confused!')
            msg.setText(f"That key didn't work, please try again! 😿\n\nError code: {response.status_code}\nMessage: {error_msg}")
            msg.setStyleSheet('''
                QMessageBox { background: #181a20; border-radius: 12px; }
                QLabel { color: #e6e6e6; font-size: 15px; }
                QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
                QPushButton:hover { background: #2563eb; }
            ''')
            msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
            msg.setWindowFlags(msg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
            msg.setWindowIcon(QIcon(cat_emoji))
            msg.exec_()

# --- Initialize PyAudio to fetch default mic info (optional) ---
# p = pyaudio.PyAudio()
# try:
#     default_index = p.get_default_input_device_info()['index']
#     mic_name = sr.Microphone.list_microphone_names()[default_index]
#     print(f"[Kitty] Listening on default device: {default_index} ({mic_name})")
# except Exception as e:
#     print(f"[Kitty] Failed to fetch default mic info: {e}")

# --- Speech-to-Text ---
# def speech_to_text(timeout=8, phrase_time_limit=10):
#     r = sr.Recognizer()
#     try:
#         with sr.Microphone() as source:
#             print("[Kitty] Adjusting for ambient noise...")
#             r.adjust_for_ambient_noise(source, duration=1)
#             print("[Kitty] Listening for your sentence...")
#             audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#         try:
#             text = r.recognize_google(audio)
#             print(f"[Kitty] You said: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("[Kitty] Could not understand audio.")
#             return ""
#         except sr.RequestError as e:
#             print(f"[Kitty] Speech recognition request failed: {e}")
#             return ""
#     except Exception as e:
#         print(f"[Kitty] Error initializing microphone: {e}")
#         return ""

# --- Text to Speech with pygame ---
# def text_to_speech(text):
#     try:
#         filename = 'kitty_tts.mp3'
#         tts = gTTS(text=text, lang='en')
#         tts.save(filename)
#
#         # Increase pitch using pydub
#         sound = AudioSegment.from_file(filename)
#         octaves = 0.5  # 0.5 = up one half-octave, 1.0 = up one octave
#         new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
#         high_pitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
#         high_pitch_sound = high_pitch_sound.set_frame_rate(44100)
#         cattish_filename = 'kitty_tts_cattish.mp3'
#         high_pitch_sound.export(cattish_filename, format='mp3')
#
#         # Play audio
#         pygame.mixer.init()
#         pygame.mixer.music.load(cattish_filename)
#         pygame.mixer.music.play()
#
#         print("[Kitty] Speaking response...")
#
#         while pygame.mixer.music.get_busy():
#             pygame.time.Clock().tick(10)
#
#         pygame.mixer.quit()
#         os.remove(filename)
#         os.remove(cattish_filename)
#         print("[Kitty] Done speaking.")
#     except Exception as e:
#         print(f"[Kitty] Failed to speak: {e}")

# --- Main loop: Capture one sentence, reply, then go again ---
if __name__ == "__main__":
    while True:
        # user_input = speech_to_text()
        # if user_input.strip():
        reply = ask_gemini("Hello Kitty!")
        #     text_to_speech(reply)
        time.sleep(1)  # Optional small delay before next listen
