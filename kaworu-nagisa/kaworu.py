import sys
import requests
from io import BytesIO
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QPoint
from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu

GIF_URL = "https://i.imgur.com/R4qdAYP.gif"  # Transparent Lain GIF

class LainCompanion(QWidget):
    def __init__(self, gif_data):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set up label with animated GIF
        self.label = QLabel(self)
        self.buffer = QBuffer()
        self.buffer.setData(QByteArray(gif_data))
        self.buffer.open(QBuffer.ReadOnly)

        self.movie = QMovie()
        self.movie.setDevice(self.buffer)
        self.label.setMovie(self.movie)
        self.movie.start()

        self.resize(self.movie.frameRect().size())

        # Position in bottom right (above taskbar)
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.width() - self.width() - 10
        y = screen.height() - self.height() - 10
        self.move(x, y)

        # Add right-click menu
        self.label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu()
        quit_action = menu.addAction("Stop Companion")
        action = menu.exec_(QCursor.pos())
        if action == quit_action:
            QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    headers = {"User-Agent": "Mozilla/5.0"}
    gif_data = requests.get(GIF_URL, headers=headers).content

    companion = LainCompanion(gif_data)
    companion.show()

    sys.exit(app.exec_())
