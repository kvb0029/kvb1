import random
import time
import unittest
import matplotlib.pyplot as plt
from datetime import datetime


class Sensor:
    """Base class for sensors."""
    def __init__(self, name):
        self.name = name
        self.value = None

    def read_data(self):
        raise NotImplementedError("Subclasses must implement read_data.")


class TemperatureSensor(Sensor):
    def read_data(self):
        self.value = random.uniform(25.0, 75.0)  # Simulated temperature in Celsius
        return self.value


class GasSensor(Sensor):
    def read_data(self):
        self.value = random.uniform(0.0, 300.0)  # Simulated gas level in ppm
        return self.value


class HumiditySensor(Sensor):
    def read_data(self):
        self.value = random.uniform(10.0, 90.0)  # Simulated humidity in percentage
        return self.value


class AlertSystem:
    """Handles alerts and notifications."""
    def __init__(self):
        self.alerts = []

    def add_alert(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alert_message = f"[{timestamp}] {message}"
        self.alerts.append(alert_message)
        print(alert_message)

    def save_alerts(self):
        with open("alerts_log.txt", "w") as file:
            file.write("\n".join(self.alerts))


class SafetySystem:
    def __init__(self):
        self.temperature_sensor = TemperatureSensor("Temperature Sensor")
        self.gas_sensor = GasSensor("Gas Sensor")
        self.humidity_sensor = HumiditySensor("Humidity Sensor")
        self.alert_system = AlertSystem()
        self.safety_status = "SAFE"
        self.logs = []

    def collect_data(self):
        temperature = self.temperature_sensor.read_data()
        gas_level = self.gas_sensor.read_data()
        humidity = self.humidity_sensor.read_data()
        return {
            "temperature": temperature,
            "gas_level": gas_level,
            "humidity": humidity
        }

    def evaluate_safety(self, data):
        alerts_triggered = []
        if data["temperature"] > 50.0:
            self.safety_status = "ALERT: High Temperature"
            alerts_triggered.append(self.safety_status)
        elif data["gas_level"] > 200.0:
            self.safety_status = "ALERT: High Gas Levels"
            alerts_triggered.append(self.safety_status)
        elif data["humidity"] < 20.0 or data["humidity"] > 80.0:
            self.safety_status = "ALERT: Unsafe Humidity"
            alerts_triggered.append(self.safety_status)
        else:
            self.safety_status = "SAFE"

        for alert in alerts_triggered:
            self.alert_system.add_alert(alert)

        return self.safety_status

    def log_data(self, data):
        log_entry = {
            "temperature": data["temperature"],
            "gas_level": data["gas_level"],
            "humidity": data["humidity"],
            "status": self.safety_status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.logs.append(log_entry)
        with open("sensor_log.csv", "a") as log_file:
            log_file.write(
                f"{log_entry['timestamp']},{log_entry['temperature']:.2f},{log_entry['gas_level']:.2f},{log_entry['humidity']:.2f},{log_entry['status']}\n"
            )

    def run_system(self, iterations=10, interval=1):
        for _ in range(iterations):
            data = self.collect_data()
            self.evaluate_safety(data)
            self.log_data(data)
            print(f"Current Status: {self.safety_status}")
            time.sleep(interval)

    def generate_report(self):
        temperatures = [log["temperature"] for log in self.logs]
        gas_levels = [log["gas_level"] for log in self.logs]
        humidity_levels = [log["humidity"] for log in self.logs]
        timestamps = [log["timestamp"] for log in self.logs]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, temperatures, label="Temperature (°C)", marker="o")
        plt.plot(timestamps, gas_levels, label="Gas Level (ppm)", marker="o")
        plt.plot(timestamps, humidity_levels, label="Humidity (%)", marker="o")
        plt.xticks(rotation=45, fontsize=8)
        plt.legend()
        plt.title("Coal Mine Safety System Report")
        plt.xlabel("Timestamp")
        plt.ylabel("Sensor Values")
        plt.tight_layout()
        plt.savefig("safety_report.png")
        print("Safety report generated: safety_report.png")


# Main program for demonstration
if __name__ == "__main__":
    system = SafetySystem()
    system.run_system(iterations=5, interval=2)
    system.generate_report()
    system.alert_system.save_alerts()

