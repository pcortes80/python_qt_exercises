import sys

from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget
)        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # Layout
        layout = QVBoxLayout()

        # Button widgets
        button1 = QPushButton("Integer")
        button1.clicked.connect(self.get_an_int)
        layout.addWidget(button1)

        button2 = QPushButton("Float")
        button2.clicked.connect(self.get_a_float)
        layout.addWidget(button2)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_an_int(self):
        my_int_value, ok = QInputDialog.getInt(
            self, "Get an integer", "Enter a number"
        )
        print("Result:", ok, my_int_value)

    def get_a_float(self):
        my_float_value, ok = QInputDialog.getDouble(
            self, "Get a float", "Enter a number"
        )
        print("Result:", ok, my_float_value)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()