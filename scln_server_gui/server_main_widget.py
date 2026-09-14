import sys
from PySide6.QtCore import QDateTime, QTimer, Qt
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QSizePolicy,
    QWidget,
    QToolBar,
    QMessageBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SCLN Server Main Window")
        self.setMinimumSize(800, 720)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.CustomizeWindowHint
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
            /* Running State (green) */
            QLabel#status_light[state="running"] {
                background-color: #55ff55;
                border: 1px solid #33cc33;
                border-radius: 2px;
            }
            /* Stopped State (Red) */
            QLabel#status_light[state="stopped"] {
                background-color: #ff5555;
                border: 1px solid #cc3333;
                border-radius: 2px;
            }
            QPushButton {
                background-color: #e1e1e1;
                border: 1px solid #adadad;
                border-radius: 3px;
                padding: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e5f1fb;
                border-color: #0078d7;
            }
            /* Dark Terminal Output Styling */
            QTextEdit#terminal_output {
                background-color: #0c0c0c;
                color: #00ff66;
                border: 1px solid #707070;
                border-radius: 3px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #888888;
                border-color: #b0b0b0;
            }
        """)

        # Track server running state
        self.is_server_running = False

        # ----------------------------------------------------
        # 0. TOP NAVIGATION TOOLBAR
        # ----------------------------------------------------
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        exit_action = QAction("Exit", self)
        about_action = QAction("About", self)
        help_action = QAction("Help", self)
        
        exit_action.triggered.connect(self.handle_exit)
        about_action.triggered.connect(self.handle_about)
        help_action.triggered.connect(self.handle_help)
        
        toolbar.addAction(exit_action)
        toolbar.addAction(about_action)
        toolbar.addAction(help_action)

        # ----------------------------------------------------
        # 1. DATE & TIME BOX CONTAINER
        # ----------------------------------------------------
        date_time_group = QGroupBox("Information")
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
        
        # Allows status_container to grow across full width inside QFormLayout
        summary_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # System Status Text + Status Light Container
        self.system_state = QLabel("STOPPED")
        
        self.status_light = QLabel()
        self.status_light.setObjectName("status_light")
        self.status_light.setFixedHeight(16)
        
        # Configure expanding policy so it resizes horizontally
        self.status_light.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.status_light.setProperty("state", "stopped")

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(8)

        # Add system status text (fixed) and status light (stretches with factor 1)
        status_layout.addWidget(self.system_state, 0)
        status_layout.addWidget(self.status_light, 1)

        summary_layout.addRow("Server State:", status_container)
        
        # ----------------------------------------------------
        # 3. SERVER CONNECTIONS CONTAINER
        # ----------------------------------------------------
        server_conn_group = QGroupBox("Server Connections")
        server_conn_layout = QHBoxLayout(server_conn_group)

        self.btn_run_server = QPushButton("Run Server")
        self.btn_stop_server = QPushButton("Stop Server")

        self.btn_stop_server.setEnabled(False)

        self.btn_run_server.clicked.connect(self.handle_run_server)
        self.btn_stop_server.clicked.connect(self.handle_stop_server)

        server_conn_layout.addWidget(self.btn_run_server)
        server_conn_layout.addWidget(self.btn_stop_server)

        # ----------------------------------------------------
        # 4. TERMINAL OUTPUT CONTAINER
        # ----------------------------------------------------
        terminal_group = QGroupBox("Server Terminal Output")
        terminal_layout = QVBoxLayout(terminal_group)

        self.terminal_output = QTextEdit()
        self.terminal_output.setObjectName("terminal_output")
        self.terminal_output.setReadOnly(True)
        
        font = QFont("Consolas" if sys.platform == "win32" else "Monospace", 10)
        self.terminal_output.setFont(font)

        terminal_layout.addWidget(self.terminal_output)

        # ----------------------------------------------------
        # MAIN LAYOUT
        # ----------------------------------------------------
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 10)
        main_layout.setSpacing(10)

        main_layout.addWidget(date_time_group)
        main_layout.addWidget(summary_group)
        main_layout.addWidget(server_conn_group)
        main_layout.addWidget(terminal_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

        self.log_info("SCLN Server Interface Initialized.")
        self.log_info("Awaiting user commands...")

    def update_clock(self):
        now = QDateTime.currentDateTime()
        self.date_label.setText(now.toString("MM/dd/yy"))
        self.time_label.setText(now.toString("hh:mm AP"))

    def log_info(self, text: str):
        """Helper to append timestamped info to the output window."""
        timestamp = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.terminal_output.append(f"[{timestamp}] {text}")

    # ----------------------------------------------------
    # SERVER CONTROL HANDLERS
    # ----------------------------------------------------
    def handle_run_server(self):
        self.is_server_running = True
        self.log_info("Starting SCLN Server daemon...")
        self.system_state.setText("RUNNING")

        self.btn_run_server.setEnabled(False)
        self.btn_stop_server.setEnabled(True)

        self.status_light.setProperty("state", "running")
        self.status_light.style().unpolish(self.status_light)
        self.status_light.style().polish(self.status_light)

    def handle_stop_server(self):
        self.is_server_running = False
        self.log_info("Stopping SCLN Server daemon...")
        self.system_state.setText("STOPPED")

        self.btn_run_server.setEnabled(True)
        self.btn_stop_server.setEnabled(False)

        self.status_light.setProperty("state", "stopped")
        self.status_light.style().unpolish(self.status_light)
        self.status_light.style().polish(self.status_light)

    # ----------------------------------------------------
    # TOOLBAR ACTION PLACEHOLDERS
    # ----------------------------------------------------
    def handle_exit(self):
        self.close()  # Leverages closeEvent below directly

    def handle_help(self):
        print("Help action triggered")

    def handle_about(self):
        print("About action triggered")

    def closeEvent(self, event):
        """Intercept window close attempts."""
        if self.is_server_running:
            QMessageBox.warning(
                self,
                "Action Blocked",
                "Cannot close application while the server is running.\nPlease stop the server first.",
                QMessageBox.StandardButton.Ok
            )
            event.ignore()
            return

        reply = QMessageBox.question(
            self,
            "Exit Confirmation",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            defaultButton=QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
            self.log_info("Exit cancelled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()