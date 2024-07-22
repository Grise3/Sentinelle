import sys
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QCheckBox, QLabel, QSpinBox, QComboBox, QPushButton, QWidget)
from PySide6.QtGui import QIcon

class ConfigWindow(QMainWindow):
    def __init__(self, config, save_config_callback):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("sentinelle.png"))
        self.config = config
        self.save_config_callback = save_config_callback

        layout = QVBoxLayout()

        # Checkboxes for enable/disable the monitoring
        self.monitor_cpu_checkbox = QCheckBox("Monitor CPU usage")
        self.monitor_ram_checkbox = QCheckBox("Monitor RAM usage")
        self.monitor_temp_checkbox = QCheckBox("Monitor the temperature")
        self.monitor_disk_checkbox = QCheckBox("Monitor free space disk")

        self.monitor_cpu_checkbox.setChecked(self.config.get("monitor_cpu", True))
        self.monitor_ram_checkbox.setChecked(self.config.get("monitor_ram", True))
        self.monitor_temp_checkbox.setChecked(self.config.get("monitor_temp", True))
        self.monitor_disk_checkbox.setChecked(self.config.get("monitor_disk", True))

        layout.addWidget(self.monitor_cpu_checkbox)
        layout.addWidget(self.monitor_ram_checkbox)
        layout.addWidget(self.monitor_temp_checkbox)
        layout.addWidget(self.monitor_disk_checkbox)

        # Spinners for alert thresholds and notification intervals
        layout.addWidget(QLabel("CPU alert treshold (%)"))
        self.cpu_threshold_spinbox = QSpinBox()
        self.cpu_threshold_spinbox.setRange(1, 100)
        self.cpu_threshold_spinbox.setValue(self.config.get("cpu_threshold", 90))
        layout.addWidget(self.cpu_threshold_spinbox)

        layout.addWidget(QLabel("RAM alert treshold (%)"))
        self.ram_threshold_spinbox = QSpinBox()
        self.ram_threshold_spinbox.setRange(1, 100)
        self.ram_threshold_spinbox.setValue(self.config.get("ram_threshold", 90))
        layout.addWidget(self.ram_threshold_spinbox)

        layout.addWidget(QLabel("Temperature alert treshold (°C)"))
        self.temp_threshold_spinbox = QSpinBox()
        self.temp_threshold_spinbox.setRange(1, 150)
        self.temp_threshold_spinbox.setValue(self.config.get("temp_threshold", 90))
        layout.addWidget(self.temp_threshold_spinbox)

        # Ajouter les options pour l'unité de température
        layout.addWidget(QLabel("Temperature unit:"))
        self.temp_unit_combo = QComboBox()
        self.temp_unit_combo.addItems(["Celsius (°C)", "Fahrenheit (°F)"])
        self.temp_unit_combo.setCurrentText(self.config.get("temperature_unit", "Celsius (°C)"))
        layout.addWidget(self.temp_unit_combo)

        # Option for show the temperature
        self.temp_display_checkbox = QCheckBox("Display temperatures")
        self.temp_display_checkbox.setChecked(self.config.get("display_temperature", True))
        layout.addWidget(self.temp_display_checkbox)

        layout.addWidget(QLabel("Disk treshold (Go)"))
        self.disk_threshold_spinbox = QSpinBox()
        self.disk_threshold_spinbox.setRange(1, 1000)
        self.disk_threshold_spinbox.setValue(self.config.get("disk_threshold", 1))
        layout.addWidget(self.disk_threshold_spinbox)

        layout.addWidget(QLabel("Check interval (s)"))
        self.check_interval_spinbox = QSpinBox()
        self.check_interval_spinbox.setRange(1, 3600)
        self.check_interval_spinbox.setValue(self.config.get("check_interval", 5))
        layout.addWidget(self.check_interval_spinbox)

        layout.addWidget(QLabel("Notification repeat interval(s)"))
        self.notification_interval_spinbox = QSpinBox()
        self.notification_interval_spinbox.setRange(1, 3600)
        self.notification_interval_spinbox.setValue(self.config.get("notification_interval", 60))
        layout.addWidget(self.notification_interval_spinbox)

        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_config(self):
        self.config["monitor_cpu"] = self.monitor_cpu_checkbox.isChecked()
        self.config["monitor_ram"] = self.monitor_ram_checkbox.isChecked()
        self.config["monitor_temp"] = self.monitor_temp_checkbox.isChecked()
        self.config["monitor_disk"] = self.monitor_disk_checkbox.isChecked()
        self.config["cpu_threshold"] = self.cpu_threshold_spinbox.value()
        self.config["ram_threshold"] = self.ram_threshold_spinbox.value()
        self.config["temp_threshold"] = self.temp_threshold_spinbox.value()
        self.config["temperature_unit"] = self.temp_unit_combo.currentText()
        self.config["display_temperature"] = self.temp_display_checkbox.isChecked()
        self.config["disk_threshold"] = self.disk_threshold_spinbox.value()
        self.config["check_interval"] = self.check_interval_spinbox.value()
        self.config["notification_interval"] = self.notification_interval_spinbox.value()
        self.save_config_callback(self.config)
        self.close()
