import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

from llmrequest import LLMRequest
from singlestreamvideo import SingleStreamVideo
from description import Description


class DescriptionUpdater(QThread):
    textUpdated = pyqtSignal(str)

    def __init__(self, description, parent=None):
        QThread.__init__(self, parent)
        self.description = description
        self.frame = None
        self.last_request_time = time.time()

    def run(self):
        current_time = time.time()
        if self.frame is not None and (current_time - self.last_request_time) >= 1:  # 1 second interval
            self.last_request_time = current_time
            self.description.update_text(self.frame)
            self.textUpdated.emit(self.description.show_text())


class VideoWindow(QMainWindow):
    def __init__(self, video: SingleStreamVideo, description: Description, stylesheet_path: str = "style.css"):
        super().__init__()

        self.video = video

        self.setWindowTitle("PyQt OpenCV Video Player")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget and Layout
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel(self)
        self.label.resize(800, 600)
        self.layout.addWidget(self.label)

        # Play Button
        self.btn_play = QPushButton("Play", self)
        # noinspection PyUnresolvedReferences
        self.btn_play.clicked.connect(self.play_video)
        self.layout.addWidget(self.btn_play)

        # Pause Button
        self.btn_pause = QPushButton("Pause", self)
        # noinspection PyUnresolvedReferences
        self.btn_pause.clicked.connect(self.pause_video)
        self.layout.addWidget(self.btn_pause)

        self.setCentralWidget(self.central_widget)

        # Description Label
        self.description_label = QLabel("Description will appear here", self)
        self.layout.addWidget(self.description_label)

        # Description Updater Thread
        self.description_updater = DescriptionUpdater(description)
        # noinspection PyUnresolvedReferences
        self.description_updater.textUpdated.connect(self.update_description_label)

        self.timer = QTimer(self)
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_frame)

        self.is_paused = False

        # Apply dark theme styles
        stylesheet = self.load_stylesheet(stylesheet_path)
        self.setStyleSheet(stylesheet)

    @staticmethod
    def load_stylesheet(file_path):
        with open(file_path, "r") as f:
            return f.read()

    def play_video(self):
        if not self.timer.isActive():
            self.timer.start(int(self.video.frame_rate))
        self.is_paused = False

    def pause_video(self):
        if self.timer.isActive():
            self.timer.stop()
        self.is_paused = True

    def update_frame(self):
        if not self.is_paused:
            frame = self.video.get_frame()
            if frame is not None:
                height, width, channel = frame.shape
                step = channel * width
                q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(q_img))

                # Update description
                self.description_updater.frame = frame
                if not self.description_updater.isRunning():
                    self.description_updater.start()

    def update_description_label(self, text):
        self.description_label.setText(text)


def main():
    app = QApplication(sys.argv)
    video = SingleStreamVideo("video.mp4")
    llm_request = LLMRequest()
    description = Description(llm_request=llm_request)
    win = VideoWindow(video, description)
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
