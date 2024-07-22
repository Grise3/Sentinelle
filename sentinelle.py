import sys
import psutil
import subprocess
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QLabel)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QTimer, QDateTime
from config_window import ConfigWindow
from stats_window import StatsWindow
from start_menu import StartMenu
from current_info_window import CurrentInfoWindow

CONFIG_FILE = 'sentinel_config.json'
STATS_FILE = 'sentinel_stats.json'

class SentinelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programme Sentinelle")
        self.setWindowIcon(QIcon("sentinelle.png"))
        self.load_config()

        # main Layout
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        pixmap = QPixmap("sentinelle.png")
        scaled_pixmap = pixmap.scaled(pixmap.width() // 12, pixmap.height() // 12)
        self.image_label.setPixmap(scaled_pixmap)

        image_layout = QHBoxLayout()
        image_layout.addStretch()
        image_layout.addWidget(self.image_label)
        image_layout.addStretch()

        layout.addLayout(image_layout)

        # buttons for enable/disable tactile screen
        self.touch_disable_button = QPushButton("Disable the touch screen")
        self.touch_enable_button = QPushButton("Enable the touch screen")
        layout.addWidget(self.touch_disable_button)
        layout.addWidget(self.touch_enable_button)

        # Connect the buttons to their
        self.touch_disable_button.clicked.connect(self.disable_touchscreen)
        self.touch_enable_button.clicked.connect(self.enable_touchscreen)

        # Button for open the Boot menu
        start_button = QPushButton("Boot menu")
        start_button.clicked.connect(self.open_start_window)
        layout.addWidget(start_button)

        # Button for open the stttings window
        config_button = QPushButton("Settings")
        config_button.clicked.connect(self.open_config_window)
        layout.addWidget(config_button)

        # Button for open the stats menu
        stats_button = QPushButton("Statistics")
        stats_button.clicked.connect(self.open_stats_window)
        layout.addWidget(stats_button)

        # Button for open the current informations window
        current_info_button = QPushButton("current informations")
        current_info_button.clicked.connect(self.open_current_info_window)
        layout.addWidget(current_info_button)

        self.grise = QLabel("Dev by Grise")
        layout.addWidget(self.grise)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize taskbar icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("sentinelle.png"))

        # Taskbar menu
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)
        self.tray_icon.setContextMenu(tray_menu)

        # Show the icon in the taskbar
        self.tray_icon.show()

        # Set the timer for the systeme monitoring
        self.timer = QTimer()
        self.timer.timeout.connect(self.monitor_system)
        self.timer.start(self.config.get("check_interval", 5) * 1000)

        # LAst time notifications were sent
        self.last_notification_times = {
            "cpu": QDateTime.currentDateTime().addSecs(-self.config.get("notification_interval", 60)),
            "ram": QDateTime.currentDateTime().addSecs(-self.config.get("notification_interval", 60)),
            "temp": QDateTime.currentDateTime().addSecs(-self.config.get("notification_interval", 60)),
            "disk": QDateTime.currentDateTime().addSecs(-self.config.get("notification_interval", 60)),
        }

    def open_pie_chart_window(self):
        self.pie_chart_window = PieChartWindow()
        self.pie_chart_window.show()

    def disable_touchscreen(self):
        if sys.platform == "linux":
            subprocess.run("xinput disable 9", shell=True)
        elif sys.platform == "win32":
            # specific command of windows for disable the touchscreen
            subprocess.run('powershell.exe -Command "Get-PnpDevice | Where-Object { $_.FriendlyName -match \'Touchscreen\' } | Disable-PnpDevice -Confirm:$false"', shell=True)

    def enable_touchscreen(self):
        if sys.platform == "linux":
            subprocess.run("xinput enable 9", shell=True)
        elif sys.platform == "win32":
            # Cspecific command of windows for enable touchscreen
            subprocess.run('powershell.exe -Command "Get-PnpDevice | Where-Object { $_.FriendlyName -match \'Touchscreen\' } | Enable-PnpDevice -Confirm:$false"', shell=True)

    def execute_command(self, command):
        # power off
        if command == "shutdown":
            if sys.platform == "linux":
                subprocess.run("shutdown now", shell=True)
            elif sys.platform == "win32":
                subprocess.run("shutdown /s /t 0", shell=True)
        # reboot
        elif command == "reboot":
            if sys.platform == "linux":
                subprocess.run("reboot", shell=True)
            elif sys.platform == "win32":
                subprocess.run("shutdown /r /t 0", shell=True)
        # sleep
        elif command == "sleep":
            if sys.platform == "linux":
                subprocess.run("systemctl suspend", shell=True)
            elif sys.platform == "win32":
                subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

    def open_config_window(self):
        self.config_window = ConfigWindow(self.config, self.save_config)
        self.config_window.show()

    def open_start_window(self):
        self.start_window = StartMenu()
        self.start_window.show()

    def open_stats_window(self):
        self.stats_window = StatsWindow()
        self.stats_window.show()

    def open_current_info_window(self):
        self.ring_stats_window = CurrentInfoWindow()
        self.ring_stats_window.show()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                self.config = json.load(file)
        else:
            # Default value if the config file does  not exist
            self.config = {
                "temperature_unit": "Celsius (°C)",
                "cpu_usage_threshold": 90, # 90%
                "ram_usage_threshold": 90, # 90%
                "disk_space_threshold": 1, # one GO
                "update_interval": 1, # one second
                "notification_interval": 3600 # one hour
            }



    def save_config(self, config):
        self.config = config
        with open(CONFIG_FILE, 'w') as file:
            json.dump(self.config, file)
        self.timer.setInterval(self.config.get("check_interval", 5) * 1000)

    def monitor_system(self):
        stats = {"timestamp": QDateTime.currentDateTime().toString()}

        if self.config.get("monitor_cpu", True):
            cpu_usage = psutil.cpu_percent()
            stats["cpu"] = cpu_usage
            if cpu_usage > self.config.get("cpu_threshold", 90):
                current_time = QDateTime.currentDateTime()
                if self.last_notification_times["cpu"].secsTo(current_time) >= self.config.get("notification_interval", 60):
                    self.tray_icon.showMessage("CPU Alert", f"Hight CPU usage : {cpu_usage}%", QSystemTrayIcon.Warning)
                    self.last_notification_times["cpu"] = current_time

        if self.config.get("monitor_ram", True):
            ram_usage = psutil.virtual_memory().percent
            stats["ram"] = ram_usage
            if ram_usage > self.config.get("ram_threshold", 90):
                current_time = QDateTime.currentDateTime()
                if self.last_notification_times["ram"].secsTo(current_time) >= self.config.get("notification_interval", 60):
                    self.tray_icon.showMessage("RAM Alert", f"Hight ram usage: {ram_usage}%", QSystemTrayIcon.Warning)
                    self.last_notification_times["ram"] = current_time

        if self.config.get("monitor_temp", True):
            temp = psutil.sensors_temperatures()
            if temp:
                temp = temp[list(temp.keys())[0]][0].current
                if self.config.get("temp_unit", "°C") == "°F":
                    temp = temp * 9/5 + 32
                stats["temp"] = temp
                if temp > self.config.get("temp_threshold", 90):
                    current_time = QDateTime.currentDateTime()
                    if self.last_notification_times["temp"].secsTo(current_time) >= self.config.get("notification_interval", 60):
                        self.tray_icon.showMessage("Temperature Alert", f"Hight temperature : {temp}°{self.config.get('temp_unit', '°C')}\n", QSystemTrayIcon.Warning)
                        self.last_notification_times["temp"] = current_time

        if self.config.get("monitor_disk", True):
            disk_usage = psutil.disk_usage('/').free / (1024 * 1024 * 1024)
            stats["disk"] = disk_usage
            if disk_usage < self.config.get("disk_threshold", 1):
                current_time = QDateTime.currentDateTime()
                if self.last_notification_times["disk"].secsTo(current_time) >= self.config.get("notification_interval", 60):
                    self.tray_icon.showMessage("Disk Alerte", f"Low free space : {disk_usage:.2f} Go", QSystemTrayIcon.Warning)
                    self.last_notification_times["disk"] = current_time

        self.save_stats(stats)

    def save_stats(self, stats):
        try:
            with open(STATS_FILE, 'r') as file:
                all_stats = json.load(file)
        except FileNotFoundError:
            all_stats = []
        all_stats.append(stats)
        with open(STATS_FILE, 'w') as file:
            json.dump(all_stats, file)

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Programme Sentinelle",
            "The application continues to run in the background. Click the taskbar icon to reopen it",
            QSystemTrayIcon.Information,
            2000
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SentinelApp()
    window.show()
    sys.exit(app.exec())
