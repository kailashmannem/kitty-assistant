from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import os

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
