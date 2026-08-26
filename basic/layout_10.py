import sys

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QLineEdit,
    QMainWindow,
    QSpinBox,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout = QFormLayout()

        self.name = QLineEdit()
        self.age = QSpinBox()
        self.icecream = QComboBox()
        self.icecream.addItems(["Vanilla", "Chocolate", "Strawberry"])

        layout.addRow("Name", self.name)
        layout.addRow("Age", self.age)
        layout.addRow("Favorite Ice Cream", self.icecream) 

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
       
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
