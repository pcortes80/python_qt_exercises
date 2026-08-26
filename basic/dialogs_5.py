import sys

from PySide6.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QPushButton
)        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, is_checked):
        button = QMessageBox.question(
            self, "Question diaglog", "The longer message"
        )

        if button == QMessageBox.StandardButton.Yes:
            print("Yes!")
        else:
            print("No!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()