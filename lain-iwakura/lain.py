import sys
import requests
from io import BytesIO
from PyQt5.QtCore import Qt, QBuffer, QByteArray, QPoint
from PyQt5.QtGui import QMovie, QCursor
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMenu

GIF_URL = "https://i.imgur.com/i5PKbBq.gif"  # Transparent Lain GIF "https://i.imgur.com/DjhYibi.gif"

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

        # Mouse dragging variables
        self.dragging = False
        self.drag_position = QPoint()
        self.locked = False

        # Enable mouse tracking for the entire widget
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.locked:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging and not self.locked:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def show_context_menu(self, pos):
        menu = QMenu()
        
        # Lock/Unlock option
        lock_text = "Unlock Position" if self.locked else "Lock Position"
        lock_action = menu.addAction(lock_text)
        
        menu.addSeparator()
        
        quit_action = menu.addAction("Stop Lain Companion")
        action = menu.exec_(QCursor.pos())
        
        if action == lock_action:
            self.locked = not self.locked
        elif action == quit_action:
            QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    headers = {"User-Agent": "Mozilla/5.0"}
    gif_data = requests.get(GIF_URL, headers=headers).content

    companion = LainCompanion(gif_data)
    companion.show()

    sys.exit(app.exec_())
