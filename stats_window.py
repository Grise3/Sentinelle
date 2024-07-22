from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer, Qt, QDateTime
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
import json
import os

STATS_FILE = 'sentinel_stats.json'
CONFIG_FILE = 'sentinel_config.json'

class StatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistics")
        self.setWindowIcon(QIcon("sentinelle.png"))
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Buttons for displa diferents statistic
        self.cpu_button = QPushButton("Display CPU statistics")
        self.cpu_button.clicked.connect(self.show_cpu_stats)
        layout.addWidget(self.cpu_button)

        self.ram_button = QPushButton("Display RAM statistics")
        self.ram_button.clicked.connect(self.show_ram_stats)
        layout.addWidget(self.ram_button)

        self.temp_button = QPushButton("Display temperature statistics")
        self.temp_button.clicked.connect(self.show_temp_stats)
        layout.addWidget(self.temp_button)

        self.disk_button = QPushButton("Display disk statistics")
        self.disk_button.clicked.connect(self.show_disk_stats)
        layout.addWidget(self.disk_button)

        # Creating the chart view
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        #Timer for the update
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_graph)
        self.update_timer.start(1000)  # Update every seconds

        self.current_series = None
        self.current_series_name = ""
        self.data = {
            "cpu": [],
            "ram": [],
            "temp": [],
            "disk": [],
            "timestamps": []
        }
        self.temp_unit = "Celsius (°C)"
        self.load_stats()
        self.load_config()

    def load_stats(self):
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as file:
                all_stats = json.load(file)

                # Initialize lists
                timestamps = []
                cpu = []
                ram = []
                temp = []
                disk = []

                for stat in all_stats:
                    timestamp = QDateTime.fromString(stat["timestamp"], "ddd MMM d HH:mm:ss yyyy")
                    if "cpu" in stat:
                        timestamps.append(timestamp)
                        cpu.append(stat["cpu"])
                    if "ram" in stat:
                        ram.append(stat["ram"])
                    if "temp" in stat:
                        temp.append(stat["temp"])
                    if "disk" in stat:
                        disk.append(stat["disk"])

                # Align all lists to the length of timestamps
                min_length = len(timestamps)

                self.data["timestamps"] = timestamps[:min_length]
                self.data["cpu"] = cpu[:min_length]
                self.data["ram"] = ram[:min_length]
                self.data["temp"] = temp[:min_length]
                self.data["disk"] = disk[:min_length]

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as file:
                config = json.load(file)
                self.temp_unit = config.get("temperature_unit", "Celsius (°C)")

    def filter_last_hour_data(self):
        current_time = QDateTime.currentDateTime()
        one_hour_ago = current_time.addSecs(-3600)

        filtered_data = {
            "timestamps": [],
            "cpu": [],
            "ram": [],
            "temp": [],
            "disk": []
        }

        for i, timestamp in enumerate(self.data["timestamps"]):
            if timestamp >= one_hour_ago:
                # Check if index is valid for all lists
                if (i < len(self.data["cpu"]) and
                    i < len(self.data["ram"]) and
                    i < len(self.data["temp"]) and
                    i < len(self.data["disk"])):
                    filtered_data["timestamps"].append(timestamp)
                    filtered_data["cpu"].append(self.data["cpu"][i])
                    filtered_data["ram"].append(self.data["ram"][i])
                    filtered_data["temp"].append(self.data["temp"][i])
                    filtered_data["disk"].append(self.data["disk"][i])

        return filtered_data

    def convert_timestamps_to_minutes(self, timestamps):
        current_time = QDateTime.currentDateTime()
        return [(current_time.toSecsSinceEpoch() - timestamp.toSecsSinceEpoch()) / 60 for timestamp in timestamps]

    def show_cpu_stats(self):
        filtered_data = self.filter_last_hour_data()
        x_data = self.convert_timestamps_to_minutes(filtered_data["timestamps"])
        self.show_chart("CPU", "CPU utilisation(%)", x_data, filtered_data["cpu"], "cpu")

    def show_ram_stats(self):
        filtered_data = self.filter_last_hour_data()
        x_data = self.convert_timestamps_to_minutes(filtered_data["timestamps"])
        self.show_chart("RAM", "RAM utilisation(%)", x_data, filtered_data["ram"], "ram")

    def show_temp_stats(self):
        filtered_data = self.filter_last_hour_data()
        x_data = self.convert_timestamps_to_minutes(filtered_data["timestamps"])
        if self.temp_unit == "Fahrenheit (°F)":
            temp_data = [self.celsius_to_fahrenheit(temp) for temp in filtered_data["temp"]]
            y_label = "Temperature (°F)"
        else:
            temp_data = filtered_data["temp"]
            y_label = "Temperature (°C)"

        self.show_chart("Temperature", y_label, x_data, temp_data, "temp")

    def show_disk_stats(self):
        filtered_data = self.filter_last_hour_data()
        x_data = self.convert_timestamps_to_minutes(filtered_data["timestamps"])
        self.show_chart("Disk", "Free space disk (Go)", x_data, filtered_data["disk"], "disk")

    def show_chart(self, title, y_label, x_data, y_data, series_name):
        chart = QChart()
        series = QLineSeries()
        series.setName(series_name)

        for x, y in zip(x_data, y_data):
            series.append(x, y)

        chart.addSeries(series)

        # Create an X axis based on minutes
        axis_x = QValueAxis()
        axis_x.setRange(0, 60)  # 0 to 60 minutes
        axis_x.setTickCount(7)  # MArkers at 0, 10, 20, 30, 40, 50, 60
        axis_x.setTitleText("Minutes")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Create Y axis
        axis_y = QValueAxis()
        axis_y.setTitleText(y_label)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        # Legende
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart.setTitle(title)
        self.chart_view.setChart(chart)
        self.current_series = series
        self.current_series_name = series_name

    def update_graph(self):
        if not self.current_series:
            return

        # Check if datas are available
        if self.current_series_name not in self.data:
            return

        filtered_data = self.filter_last_hour_data()
        x_data = self.convert_timestamps_to_minutes(filtered_data["timestamps"])
        if self.current_series_name == "temp" and self.temp_unit == "Fahrenheit (°F)":
            y_data = [self.celsius_to_fahrenheit(temp) for temp in filtered_data["temp"]]
        else:
            y_data = filtered_data[self.current_series_name]

        self.current_series.clear()
        for x, y in zip(x_data, y_data):
            self.current_series.append(x, y)

    def celsius_to_fahrenheit(self, celsius):
        return celsius * 9/5 + 32
