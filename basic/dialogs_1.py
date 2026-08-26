import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QDialog
)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton("Press me for a dialog!")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, is_checked):
        print("Click", is_checked)

        dlg = QDialog(self)
        dlg.setWindowTitle("?")
        dlg.exec()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()