import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QToolBar
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        label = QLabel("Hello")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        # Optional: to prevent the toolbar being removed.
        # toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(toolbar)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()