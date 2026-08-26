import sys

from PySide6.QtCore import (
    QDateTime,
    QTimer
)

from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynalene Main Widget")


        # 1. Real-time Date and Time Labels
        self.date_label = QLabel()
        self.time_label = QLabel()

        # Timer to update both labels every second (1000 ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        # Initial call to populate immediately on startup
        self.update_clock()

        # User Widgets
        self.select_user = QComboBox()
        self.system_state = QLabel("INITILIZED")
        self.selected_user = QLabel("Operator")
        self.switch_user = QPushButton("Switch User")
        self.logout = QPushButton("Logout")
        self.select_user.addItems(["Operator", "Engineer", "Admin"])

        # Connections
        self.switch_user.clicked.connect(self.handle_switch_user)
        self.logout.clicked.connect(self.handle_logout)

        # Layout Setup
        layout = QFormLayout()

        # Layout
        layout.addRow("Date", self.date_label)
        layout.addRow("Time", self.time_label)
        layout.addRow("System State:", self.system_state)
        layout.addRow("User Profile", self.selected_user) 
        layout.addRow("Users", self.select_user)
        layout.addRow(self.switch_user)
        layout.addRow(self.logout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_clock(self):
        now = QDateTime.currentDateTime()
        
        # Format: "MM/dd/yy"
        self.date_label.setText(now.toString("MM/dd/yy"))

        # Format: "hh:mm AP"
        self.time_label.setText(now.toString("hh:mm AP"))

    def handle_users_changed(self, selected_users):
        print(selected_users)

    def handle_switch_user(self):
        current_selection = self.select_user.currentText()
        if current_selection == "Operator":
            self.selected_user.setText("Operator")
            print("Operator")
        elif current_selection == "Engineer":
            self.selected_user.setText("Engineer")
        elif current_selection == "Admin":
            self.selected_user.setText("Admin")

    def handle_logout(self):
        print("Logout")
       
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
