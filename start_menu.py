import subprocess
import os
import platform
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon

class StartMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Boot menu")
        self.setWindowIcon(QIcon("sentinelle.png"))
        self.setGeometry(100, 100, 200, 200)

        layout = QVBoxLayout()

        self.sleep_button = QPushButton("Sleep")
        self.sleep_button.clicked.connect(self.sleep)
        layout.addWidget(self.sleep_button)

        self.shutdown_button = QPushButton("Shutdown")
        self.shutdown_button.clicked.connect(self.shutdown)
        layout.addWidget(self.shutdown_button)

        self.restart_button = QPushButton("Reboot")
        self.restart_button.clicked.connect(self.restart)
        layout.addWidget(self.restart_button)

        self.logout_button = QPushButton("Disconnect")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def sleep(self):
        os_type = platform.system()
        try:
            if os_type == 'Linux':
                subprocess.run(['systemctl', 'suspend'])
            elif os_type == 'Windows':
                subprocess.run(['shutdown', '/h'])
        except Exception as e:
            print(f"Error when going to sleep : {e}")

    def shutdown(self):
        os_type = platform.system()
        try:
            if os_type == 'Linux':
                subprocess.run(['systemctl', 'poweroff'])
            elif os_type == 'Windows':
                subprocess.run(['shutdown', '/s', '/f', '/t', '0'])
        except Exception as e:
            print(f"Error during shutdown : {e}")

    def restart(self):
        os_type = platform.system()
        try:
            if os_type == 'Linux':
                subprocess.run(['systemctl', 'reboot'])
            elif os_type == 'Windows':
                subprocess.run(['shutdown', '/r', '/f', '/t', '0'])
        except Exception as e:
            print(f"Error during reboot : {e}")

    def logout(self):
        os_type = platform.system()
        try:
            if os_type == 'Linux':
                subprocess.run(['pkill', '-KILL', '-u', os.getlogin()])
            elif os_type == 'Windows':
                subprocess.run(['shutdown', '/l'])
        except Exception as e:
            print(f"Error during disconnect :{e}")


