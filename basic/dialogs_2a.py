import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel
)
class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")
        
        buttons = (
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)       
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def button_clicked(self, is_checked):
        print("Click", is_checked)

        dlg = CustomDialog()
        if dlg.exec():
            print("OK")
        else:
            print("Cancel")

app = QApplication(sys.argv)
window = CustomDialog()
window.show()
app.exec()