import sys
import psutil
import json
import os
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QLabel, QProgressBar, QApplication)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

CONFIG_FILE = 'sentinel_config.json'
STATS_FILE = 'sentinel_stats.json'

class CurrentInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real time statistics")
        self.setWindowIcon(QIcon("sentinelle.png"))
        self.setGeometry(100, 100, 600, 400)

        # Loading the configuration
        self.config = self.load_config()

        layout = QVBoxLayout()

        # Creation of the progress bar widgets
        self.cpu_label = QLabel("CPU utilisation:")
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.cpu_progress)

        self.ram_label = QLabel("RAM utilisation:")
        self.ram_progress = QProgressBar()
        self.ram_progress.setRange(0, 100)
        layout.addWidget(self.ram_label)
        layout.addWidget(self.ram_progress)

        self.temp_label = QLabel("Tempdrature :")
        self.temp_display = QLabel()
        layout.addWidget(self.temp_label)
        layout.addWidget(self.temp_display)

        self.disk_label = QLabel("Space Disk :")
        self.disk_progress = QProgressBar()
        self.disk_progress.setRange(0, 100)
        layout.addWidget(self.disk_label)
        layout.addWidget(self.disk_progress)

        # Timer for progress bar update
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_progress)
        self.update_timer.start(self.config.get("update_interval", 5000))  # Update evey 5 seconds

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            return {
                "temperature_unit": "Celsius (°C)",
                "cpu_usage_threshold": 90,
                "ram_usage_threshold": 90,
                "disk_space_threshold": 1,
                "update_interval": 5000,  # 5 secondes
                "notification_interval": 60000  # 1 minute
            }

    def update_progress(self):
        # Update the CPU utilisation
        cpu_usage = psutil.cpu_percent()
        self.cpu_progress.setValue(cpu_usage)

        # Update the RAM utilisation
        ram_usage = psutil.virtual_memory().percent
        self.ram_progress.setValue(ram_usage)

        # Update the temperature
        temp = psutil.sensors_temperatures()
        if temp:
            temp_value = temp[list(temp.keys())[0]][0].current
            if self.config.get("temperature_unit") == "Fahrenheit (°F)":
                temp_value = temp_value * 9/5 + 32
            self.temp_display.setText(f"Temperature: {temp_value:.1f} {self.config.get('temperature_unit')}")
        else:
            self.temp_display.setText("Temperature: Unavailable")

        # Update Space disk
        disk_usage = psutil.disk_usage('/').percent
        self.disk_progress.setValue(disk_usage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrentInfoWindow()
    window.show()
    sys.exit(app.exec())
