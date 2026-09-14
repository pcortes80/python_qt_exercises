import sys
from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QMessageBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynalene Main Widget")
        self.setMinimumSize(300, 560)   # width, height
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
        )

        # Style sheet to mimic classic native desktop look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e8e8e8;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #b0b0b0;
                border-radius: 4px;
                margin-top: 10px;
                background-color: #f0f0f0;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 4px;
            }
            /* Status Light Square Style */
            QLabel#status_light {
                background-color: #55ff55;
                border: 1px solid #33cc33;
                border-radius: 2px;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #b0b0b0;
                font-size: 13px;
            }
            QListWidget::item:selected {
                background-color: #2b82c5;
                color: #ffffff;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e5f1fb;
                border-color: #0078d7;
            }
        """)

        # ----------------------------------------------------
        # 0. TOP NAVIGATION TOOLBAR
        # ----------------------------------------------------
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Create Toolbar Actions
        exit_action = QAction("Exit", self)
        connect_action = QAction("Connect", self)
        disconnect_action = QAction("Disconnect", self)
        settings_action = QAction("Settings", self)

        # Connect placeholders (signals)
        exit_action.triggered.connect(self.handle_exit)
        connect_action.triggered.connect(self.handle_connect)
        disconnect_action.triggered.connect(self.handle_disconnect)
        settings_action.triggered.connect(self.handle_settings)

        # Add actions to toolbar
        toolbar.addAction(exit_action)
        toolbar.addAction(connect_action)
        toolbar.addAction(disconnect_action)
        toolbar.addAction(settings_action)

        # ----------------------------------------------------
        # 1. DATE & TIME BOX CONTAINER
        # ----------------------------------------------------
        date_time_group = QGroupBox()
        date_time_layout = QFormLayout(date_time_group)
        date_time_layout.setLabelAlignment(Qt.AlignLeft)

        self.date_label = QLabel()
        self.time_label = QLabel()

        date_time_layout.addRow("Date:", self.date_label)
        date_time_layout.addRow("Time:", self.time_label)

        # ----------------------------------------------------
        # 2. SUMMARY BOX CONTAINER
        # ----------------------------------------------------
        summary_group = QGroupBox("Summary")
        summary_layout = QFormLayout(summary_group)
        summary_layout.setLabelAlignment(Qt.AlignLeft)

        # System Status Text + Status Light Container
        self.system_state = QLabel("INITIALIZED")
        
        self.status_light = QLabel()
        self.status_light.setObjectName("status_light")
        self.status_light.setFixedSize(60, 16)  # Width, Height

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)
        
        status_layout.addWidget(self.system_state)
        status_layout.addWidget(self.status_light)
        status_layout.addStretch()  # Keeps light next to the text

        # User Profile and Dropdown
        self.selected_user = QLabel("Operator")
        self.select_user = QComboBox()
        self.select_user.addItems(["Operator", "Engineer", "Admin"])

        # Add fields to Summary box
        summary_layout.addRow("System State:", status_container)
        summary_layout.addRow("User Profile:", self.selected_user)
        summary_layout.addRow("Users:", self.select_user)

        # Action Buttons
        self.switch_user = QPushButton("Switch User")
        self.logout = QPushButton("Logout")

        # ----------------------------------------------------
        # 3. COMMAND / ACTION LIST BOX
        # ----------------------------------------------------
        self.command_list = QListWidget()
        commands = [
            "General Commands",
            "Commands",
            "Alarms",
            "Cabinet Management",
            "Thermal Summary",
            "User Interface (UI)",
            "Air Handling",
            "PID",
            "Sensors",
            "Chillers & Pumps",
            "Configurations",
            "Errors",
            "Logs"
        ]
        self.command_list.addItems(commands)
        self.command_list.setCurrentRow(0)

        # Connect signals
        self.switch_user.clicked.connect(self.handle_switch_user)
        self.logout.clicked.connect(self.handle_logout)

        # ----------------------------------------------------
        # MAIN LAYOUT
        # ----------------------------------------------------
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 10)
        main_layout.setSpacing(10)

        main_layout.addWidget(date_time_group)
        main_layout.addWidget(summary_group)
        main_layout.addWidget(self.switch_user)
        main_layout.addWidget(self.logout)
        main_layout.addWidget(self.command_list)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Setup clock timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = QDateTime.currentDateTime()
        self.date_label.setText(now.toString("MM/dd/yy"))
        self.time_label.setText(now.toString("hh:mm AP"))

    def handle_switch_user(self):
        current_selection = self.select_user.currentText()
        self.selected_user.setText(current_selection)

    def handle_logout(self):
        print("Logout clicked")

    # ----------------------------------------------------
    # TOOLBAR ACTION PLACEHOLDERS
    # ----------------------------------------------------
    def handle_exit(self):
        print("Exit action triggered")
        reply = QMessageBox.question(
            self,
            "Exit Confirmation",    # Window Tittle
            "Are you sure you want to exit?",   # Message Text
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No   # Default focused button
        )

        #Check wich button the user clicked
        if reply == QMessageBox.StandardButton.Yes:
            print("Exiting...")
            sys.exit()
        else:
            print("Not exiting...")

    def handle_connect(self):
        print("Connect action triggered")

    def handle_disconnect(self):
        print("Disconnect action triggered")

    def handle_settings(self):
        print("Settings action triggered")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()