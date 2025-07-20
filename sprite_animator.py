from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import os
from cryptography.fernet import Fernet
from PyQt5.QtCore import QBuffer, QByteArray, QIODevice

class SpriteAnimator:
    def __init__(self, label, image_path, frame_width, frame_height, frame_count, scale=3):
        self.label = label
        self.image_path = image_path
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.scale = scale

        self.frames = []
        self.frame_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.load_frames()

    def load_frames(self):
        self.frames = []
        if self.image_path.endswith('.enc'):
            # Always look for the key in assets_enc/key.key relative to this script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            key_path = os.path.join(base_dir, 'assets_enc', 'key.key')
            with open(key_path, 'rb') as kf:
                key = kf.read()
            cipher = Fernet(key)
            with open(self.image_path, 'rb') as ef:
                encrypted_data = ef.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            # Load QPixmap from decrypted bytes
            ba = QByteArray(decrypted_data)
            buffer = QBuffer(ba)
            buffer.open(QIODevice.ReadOnly)
            sprite_sheet = QPixmap()
            sprite_sheet.loadFromData(ba, 'PNG')
        else:
            full_path = os.path.abspath(self.image_path)
            sprite_sheet = QPixmap(full_path)
        for i in range(self.frame_count):
            frame = sprite_sheet.copy(i * self.frame_width, 0, self.frame_width, self.frame_height)
            frame = frame.scaled(self.frame_width * self.scale,
                                 self.frame_height * self.scale,
                                 Qt.KeepAspectRatio,
                                 Qt.SmoothTransformation)
            self.frames.append(frame)

    def start(self, interval=100):
        if not self.frames:
            return
        self.frame_index = 0
        self.label.setPixmap(self.frames[self.frame_index])
        self.label.resize(self.frames[self.frame_index].size())
        self.timer.start(interval)

    def stop(self):
        self.timer.stop()

    def update_frame(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.label.setPixmap(self.frames[self.frame_index])
