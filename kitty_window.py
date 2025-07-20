import random
import pyautogui
from PyQt5.QtCore import Qt, QTimer, QDateTime, QPoint, pyqtSlot, QMetaObject, Q_ARG, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QDialog, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
import threading
from kitty_genai import ask_gemini
# , text_to_speech, speech_to_text
from sprite_animator import SpriteAnimator
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap
from PyQt5.QtCore import QThread
# import os
# import pygame

class ChatDialog(QDialog):
    response_ready = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Kitty Chat')
        # Set cat emoji as window icon
        cat_emoji = QPixmap(64, 64)
        cat_emoji.fill(Qt.transparent)
        painter = QPainter(cat_emoji)
        font = self.font()
        font.setPointSize(32)
        painter.setFont(font)
        painter.drawText(cat_emoji.rect(), Qt.AlignCenter, '🐱')
        painter.end()
        self.setWindowIcon(QIcon(cat_emoji))
        self.setMinimumSize(380, 100)
        self.setMaximumSize(380, 320)
        self.setFixedWidth(380)
        # self.setFixedSize(340, 260)  # Remove fixed size
        self.setSizeGripEnabled(False)
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setStyleSheet('''
            background: #23272e;
            color: #e6e6e6;
            border-radius: 8px;
            padding: 8px;
            font-size: 15px;
            font-family: Consolas, monospace;
        ''')
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText('Type your message...')
        self.input_line.setStyleSheet('''
            background: #181a20;
            color: #fff;
            border: 1px solid #444;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
        ''')
        # self.send_btn = QPushButton('Send', self)
        # self.send_btn.setStyleSheet('''
        #     QPushButton {
        #         background: #3b82f6;
        #         color: #fff;
        #         border: none;
        #         border-radius: 6px;
        #         padding: 6px 18px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background: #2563eb;
        #     }
        # ''')
        layout.addWidget(self.text_edit)
        layout.addWidget(self.input_line)
        # layout.addWidget(self.send_btn)
        # self.send_btn.clicked.connect(self.send_message)
        self.input_line.returnPressed.connect(self.send_message)
        self.response_ready.connect(self.append_response)
        self.setStyleSheet('''
            QDialog {
                background: #181a20;
                border-radius: 12px;
            }
        ''')
        # Remove '?' help button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.adjust_dialog_size()

    def send_message(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return
        self.text_edit.clear()
        self.text_edit.append(f'<span style="color:#a5d6fa;"><b>You:</b> {user_text}</span>')
        self.input_line.clear()
        self.text_edit.append('<span style="color:#b5b5b5;">Kitty: ...</span>')
        self.adjust_dialog_size()

        def get_response():
            try:
                # print("get_response called with:", user_text)
                system_prompt = (
                    "Reply as a playful cat named Kitty. Use cat sounds like 'meow' or 'purr' sometimes. Keep your responses short and adorable."
                )
                full_prompt = f"{system_prompt}\nUser: {user_text}"
                response = ask_gemini(full_prompt)
                # print("Gemini response:", response)
                self.response_ready.emit(f'<span style=\"color:#f9c97a;\"><b>Kitty:</b> {response}</span>')
            except Exception as e:
                print("Exception in get_response:", e)

        threading.Thread(target=get_response, daemon=True).start()

    def append_response(self, text):
        # Only keep the latest user and kitty message
        lines = self.text_edit.toHtml().split('<br />')
        # Find the last user message
        user_line = next((l for l in reversed(lines) if 'You:' in l), None)
        # The last line is always the kitty message
        kitty_line = text
        self.text_edit.clear()
        if user_line:
            self.text_edit.append(user_line)
        self.text_edit.append(kitty_line)
        self.adjust_dialog_size()

    def adjust_dialog_size(self):
        self.text_edit.document().adjustSize()
        doc_height = self.text_edit.document().size().height()
        input_height = self.input_line.sizeHint().height()
        margin = 60
        new_height = int(doc_height) + input_height + margin
        new_height = max(120, min(new_height, 320))
        self.setFixedSize(self.width(), new_height)

    def truncate_to_fit(self):
        # Remove lines from the top until all content fits without scrollbars
        doc = self.text_edit.document()
        max_height = self.text_edit.viewport().height()
        while doc.size().height() > max_height and doc.blockCount() > 1:
            cursor = self.text_edit.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.LineUnderCursor)
            cursor.removeSelectedText()
            cursor.deleteChar()  # Remove the newline

# class VoiceAnalyzerWidget(QWidget):
#     def __init__(self, parent=None, bar_count=8):
#         super().__init__(parent)
#         self.bar_count = bar_count
#         self.bars = [10] * bar_count
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.animate)
#         self.setFixedSize(60, 20)
#         self.hide()
#
#     def animate(self):
#         self.bars = [random.randint(5, 18) for _ in range(self.bar_count)]
#         self.update()
#
#     def start(self):
#         self.show()
#         self.timer.start(80)
#
#     def stop(self):
#         self.timer.stop()
#         self.hide()
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         bar_width = self.width() // self.bar_count
#         for i, h in enumerate(self.bars):
#             painter.setBrush(QColor(0, 200, 255))
#             painter.setPen(Qt.NoPen)
#             x = i * bar_width + 2
#             y = self.height() - h
#             painter.drawRect(x, y, bar_width - 4, h)

class KittyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set cat emoji as window icon
        cat_emoji = QPixmap(64, 64)
        cat_emoji.fill(Qt.transparent)
        painter = QPainter(cat_emoji)
        font = self.font()
        font.setPointSize(32)
        painter.setFont(font)
        painter.drawText(cat_emoji.rect(), Qt.AlignCenter, '🐱')
        painter.end()
        self.setWindowIcon(QIcon(cat_emoji))
        self.current_state = None
        self.is_sleeping = False
        self.dragging = False
        self.offset = QPoint(0, 0)
        self._stop_listening = threading.Event()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.last_mouse_pos = pyautogui.position()
        self.last_mouse_move_time = QDateTime.currentDateTime()

        self.label = QLabel(self)
        self.label.setScaledContents(True)

        self.animations = {
            "idle_left": SpriteAnimator(self.label, "assets/idle_left.png", 32, 32, 4),
            "idle_right": SpriteAnimator(self.label, "assets/idle_right.png", 32, 32, 4),
            "walk_left": SpriteAnimator(self.label, "assets/walk_left.png", 32, 32, 16),
            "walk_right": SpriteAnimator(self.label, "assets/walk_right.png", 32, 32, 16),
            "dance_left": SpriteAnimator(self.label, "assets/dance_left.png", 32, 32, 8),
            "dance_right": SpriteAnimator(self.label, "assets/dance_right.png", 32, 32, 8),
            "sleep_left": SpriteAnimator(self.label, "assets/sleep_left.png", 32, 32, 4),
            "sleep_right": SpriteAnimator(self.label, "assets/sleep_right.png", 32, 32, 4),
            "jump_left": SpriteAnimator(self.label, "assets/jump_left.png", 32, 32, 7),
            "jump_right": SpriteAnimator(self.label, "assets/jump_right.png", 32, 32, 7),
        }

        self.setFixedSize(64, 64)
        self.move_to_bottom_right()

        self.mouse_idle_timer = QTimer(self)
        self.mouse_idle_timer.timeout.connect(self.check_mouse_idle)
        self.mouse_idle_timer.start(1000)

        self.behavior_timer = QTimer(self)
        self.behavior_timer.timeout.connect(self.random_action)
        self.behavior_timer.start(3000)

        self.last_walk_time = QDateTime.currentDateTime().addSecs(-20)
        self.last_jump_time = QDateTime.currentDateTime().addSecs(-20)
        self.set_state("idle")

        # self.listening_label = QLabel('Kitty: I am listening...', self)
        # self.listening_label.setStyleSheet('background: #222; color: #fff; border-radius: 8px; padding: 4px; font-size: 12px;')
        # self.listening_label.adjustSize()
        # self.listening_label.move((self.width() - self.listening_label.width()) // 2, -20)
        # self.listening_label.hide()

        # self.voice_analyzer = VoiceAnalyzerWidget(self)
        # self.voice_analyzer.move((self.width() - self.voice_analyzer.width()) // 2, -self.voice_analyzer.height() - 8)

        self._single_click_timer = QTimer(self)
        self._single_click_timer.setSingleShot(True)
        self._single_click_timer.timeout.connect(self._handle_single_click)
        self._pending_single_click_event = None
        self._double_click_detected = False
        self._mouse_dragged = False
        # self._voice_active = False
        # pygame.mixer.init()
        # threading.Thread(target=self.continuous_listen_loop, daemon=True).start()
        self._single_click_timer.setInterval(250)  # Reduce latency to 100ms

    # def continuous_listen_loop(self):
    #     while not self._stop_listening.is_set():
    #         if self._voice_active:
    #             continue
    #         self._voice_active = True
    #         self.show_listening_indicator()
    #         try:
    #             user_text = speech_to_text()
    #             if not self._stop_listening.is_set() and user_text:
    #                 response = ask_gemini(user_text)
    #                 text_to_speech(response)
    #         except Exception as e:
    #             print(f"[ERROR] {e}")
    #         self.hide_listening_indicator()
    #         self._voice_active = False

    # def cancel_voice_interaction(self):
    #     self._stop_listening.set()
    #     self.hide_listening_indicator()
    #     self._interaction_active = False
    #     self.set_state("idle")


    def get_facing_direction(self):
        return "left" if self.x() < QApplication.primaryScreen().geometry().width() // 2 else "right"

    def set_state(self, state):
        if QThread.currentThread() != QApplication.instance().thread():
            QMetaObject.invokeMethod(self, '_set_state_main', Qt.QueuedConnection, Q_ARG(str, state))
            return
        self._set_state_main(state)

    @pyqtSlot(str)
    def _set_state_main(self, state):
        if getattr(self, '_interaction_active', False):
            state = "idle"
        dir_ = self.get_facing_direction()
        new = f"{state}_{dir_}"
        if new == self.current_state:
            return
        if self.is_sleeping and not (state.startswith("idle") or state == "sleep"):
            return
        if self.current_state in self.animations:
            self.animations[self.current_state].stop()
        self.current_state = new
        self.animations[new].start()

    def sleep(self):
        if not self.is_sleeping:
            self.is_sleeping = True
            self.set_state("sleep")

    def wake_up(self):
        if self.is_sleeping:
            self.is_sleeping = False
            self.set_state("idle")

    def check_mouse_idle(self):
        pos = pyautogui.position()
        if pos != self.last_mouse_pos:
            self.last_mouse_pos = pos
            self.last_mouse_move_time = QDateTime.currentDateTime()
            self.wake_up()
        else:
            elapsed = self.last_mouse_move_time.msecsTo(QDateTime.currentDateTime())
            if elapsed >= 5000:
                self.sleep()

    def random_action(self):
        if getattr(self, '_interaction_active', False):
            return
        if self.is_sleeping:
            return
        now = QDateTime.currentDateTime()
        mpos = pyautogui.position()
        if mpos.y < self.y() and self.last_jump_time.msecsTo(now) >= 20000:
            self.last_jump_time = now
            self.set_state("jump")
            dir_ = self.get_facing_direction()
            dx = 20 if dir_ == "left" else -20
            steps = 7
            jump_height = 100
            start_x, start_y = self.x(), self.y()
            sw = QApplication.primaryScreen().geometry().width()

            def parabolic_jump(step):
                if step > steps:
                    final_x = min(max(start_x + dx * steps, 0), sw - self.width())
                    self.move(final_x, start_y)
                    self.set_state("idle")
                    return
                t = step / steps
                x = start_x + dx * step
                y = start_y - int(-4 * jump_height * (t - 0.5) ** 2 + jump_height)
                x = min(max(x, 0), sw - self.width())
                self.move(x, y)
                QTimer.singleShot(50, lambda: parabolic_jump(step + 1))

            parabolic_jump(0)
            return
        if self.last_walk_time.msecsTo(now) >= 15000:
            self.last_walk_time = now
            self.perform_walk()
            return
        self.set_state(random.choice(["idle", "dance"]))

    def perform_walk(self):
        dir_ = self.get_facing_direction()
        dx = -10 if dir_ == "right" else 10
        self.set_state("walk")

        def step(i):
            if i >= 7:
                self.set_state("idle")
                return
            sw = QApplication.primaryScreen().geometry().width()
            nx = min(max(self.x() + dx, 0), sw - self.width())
            self.move(nx, self.y())
            QTimer.singleShot(100, lambda: step(i + 1))

        step(0)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.RightButton:
            self.show_context_menu(ev.globalPos())
            return
        if ev.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = ev.pos()
            self._click_pos = ev.pos()
            self._click_time = QDateTime.currentDateTime()
            self._mouse_dragged = False
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self.dragging:
            self.move(ev.globalPos() - self.offset)
            self._mouse_dragged = True
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            if self.dragging:
                self.dragging = False
                if (ev.pos() - self._click_pos).manhattanLength() < 5 and not self._mouse_dragged:
                    self._pending_single_click_event = ev
                    self._single_click_timer.start(400)
        super().mouseReleaseEvent(ev)

    def mouseDoubleClickEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._double_click_detected = True
            self._single_click_timer.stop()
            self._pending_single_click_event = None
            self._mouse_dragged = False
            # if not self._voice_active:
            #     self.start_voice_interaction()
            # else:
            #     self.cancel_voice_interaction()
        super().mouseDoubleClickEvent(ev)

    @pyqtSlot()
    def _handle_single_click(self):
        if not self._double_click_detected and not self._mouse_dragged:
            self.open_chat_dialog()
        self._pending_single_click_event = None
        self._double_click_detected = False
        self._mouse_dragged = False

    def open_chat_dialog(self):
        self._interaction_active = True
        self.set_state("idle")
        dlg = ChatDialog(self)
        # Position the dialog on the opposite side of the kitty
        kitty_geom = self.geometry()
        screen_geom = QApplication.primaryScreen().geometry()
        dlg_geom = dlg.frameGeometry()
        if kitty_geom.center().x() > screen_geom.width() // 2:
            # Kitty is on the right, show dialog to the left
            x = max(kitty_geom.left() - dlg.width() - 20, 0)
        else:
            # Kitty is on the left, show dialog to the right
            x = kitty_geom.right() + 20
        y = max(kitty_geom.top() - dlg.height() // 2, 0)
        dlg.move(x, y)
        dlg.exec_()
        self._interaction_active = False
        self.set_state("idle")

    # def show_listening_indicator(self):
    #     QMetaObject.invokeMethod(self, '_show_listening_indicator', Qt.QueuedConnection)

    # @pyqtSlot()
    # def _show_listening_indicator(self):
    #     self.listening_label.show()
    #     self.listening_label.raise_()
    #     self.voice_analyzer.start()
    #     meow_path = 'assets/meow.wav'
    #     if os.path.exists(meow_path):
    #         pygame.mixer.music.load(meow_path)
    #         pygame.mixer.music.play()

    # def hide_listening_indicator(self):
    #     QMetaObject.invokeMethod(self, '_hide_listening_indicator', Qt.QueuedConnection)

    # @pyqtSlot()
    # def _hide_listening_indicator(self):
    #     self.listening_label.hide()
    #     self.voice_analyzer.stop()

    # def start_voice_interaction(self):
    #     def run():
    #         self._interaction_active = True
    #         self._voice_active = True
    #         self.set_state("idle")
    #         while self._voice_active:
    #             self.show_listening_indicator()
    #             try:
    #                 user_text = speech_to_text()
    #                 if self._voice_active and user_text:
    #                     response = ask_gemini(user_text)
    #                     text_to_speech(response)
    #             except Exception as e:
    #                 print(f"[ERROR] {e}")
    #             self.hide_listening_indicator()
    #         self._interaction_active = False
    #         self.set_state("idle")
    #
    #     threading.Thread(target=run, daemon=True).start()

    # def cancel_voice_interaction(self):
    #     self._voice_active = False
    #     self.hide_listening_indicator()
    #     self._interaction_active = False
    #     self.set_state("idle")

    def move_to_bottom_right(self):
        geom = QApplication.primaryScreen().availableGeometry()
        margin = 60
        x = geom.right() - self.width() - margin
        y = geom.bottom() - self.height() - margin
        self.move(x, y)

    def show_context_menu(self, pos):
        from PyQt5.QtWidgets import QMenu, QApplication
        menu = QMenu()
        api_action = menu.addAction('API Key')
        exit_action = menu.addAction('Exit')
        action = menu.exec_(pos)
        if action == api_action:
            from kitty_genai import prompt_for_api_key, get_gemini_api_url
            import requests
            from PyQt5.QtWidgets import QMessageBox, QApplication
            from PyQt5.QtGui import QIcon, QPixmap, QPainter
            from PyQt5.QtCore import Qt
            kitty_geom = self.geometry()
            screen_geom = QApplication.primaryScreen().geometry()
            while True:
                # Calculate position for the dialog
                if kitty_geom.center().x() > screen_geom.width() // 2:
                    # Kitty is on the right, show dialog to the left
                    x = max(kitty_geom.left() - 380 - 20, 0)
                else:
                    # Kitty is on the left, show dialog to the right
                    x = kitty_geom.right() + 20
                y = max(kitty_geom.top() - 100, 0)
                new_key = prompt_for_api_key(exit_on_cancel=False, pos=(x, y))
                if not new_key:
                    print("API key dialog closed or cancelled, app continues running.")
                    break
                # Validate the key by sending a test prompt
                url = get_gemini_api_url(new_key)
                headers = {'Content-Type': 'application/json'}
                data = {"contents": [{"parts": [{"text": "Hello"}]}]}
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 200:
                    import kitty_genai
                    kitty_genai.GEMINI_API_KEY = new_key
                    kitty_genai.GEMINI_API_URL = url
                    break
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle('Kitty Confused!')
                    try:
                        error_json = response.json()
                        error_msg = error_json["error"]["message"]
                        if not error_msg:
                            error_msg = 'Unknown error'
                    except Exception:
                        error_msg = 'Unknown error'
                    msg.setText(f"Kitty code denied 😿\n\nError code: {response.status_code}\nMessage: {error_msg}")
                    msg.setStyleSheet('''
                        QMessageBox { background: #181a20; border-radius: 12px; }
                        QLabel { color: #e6e6e6; font-size: 15px; }
                        QPushButton { background: #3b82f6; color: #fff; border: none; border-radius: 6px; padding: 6px 18px; font-size: 14px; }
                        QPushButton:hover { background: #2563eb; }
                    ''')
                    msg.setWindowFlags(msg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
                    msg.setWindowFlags(msg.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                    cat_emoji = QPixmap(64, 64)
                    cat_emoji.fill(Qt.transparent)
                    painter = QPainter(cat_emoji)
                    font = QApplication.instance().font()
                    font.setPointSize(32)
                    painter.setFont(font)
                    painter.drawText(cat_emoji.rect(), Qt.AlignCenter, '🐱')
                    painter.end()
                    msg.setWindowIcon(QIcon(cat_emoji))
                    msg.exec_()
        elif action == exit_action:
            QApplication.quit()