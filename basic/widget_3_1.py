import sys
from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QCheckBox, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        # Container widget & vertical layout for multiple items
        container = QWidget()
        layout = QVBoxLayout()

        self.checkboxes = []

        # Create 5 check boxes dynamically
        for i in range(1, 6):
            cb = QCheckBox(f"Alarm {i}")
            if i == 1:
                cb.setCheckState(Qt.CheckState.Checked)

            # Pass the check box name along with the state using partial
            cb.stateChanged.connect(partial(self.show_state, cb.text()))

            layout.addWidget(cb)
            self.checkboxes.append(cb)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_state(self, name, state):
        is_checked = Qt.CheckState(state) == Qt.CheckState.Checked

        if state == Qt.CheckState.Checked.value:
            print(f"{name}: Checked")
        elif state == Qt.CheckState.Unchecked.value:
            print(f"{name}: Unchecked")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()