import unittest
from cmcss import SafetySystem


class TestCoalMineSafetySystem(unittest.TestCase):
    def setUp(self):
        self.system = SafetySystem()

    def test_temperature_sensor(self):
        value = self.system.temperature_sensor.read_data()
        self.assertTrue(25.0 <= value <= 75.0, "Temperature out of range")

    def test_gas_sensor(self):
        value = self.system.gas_sensor.read_data()
        self.assertTrue(0.0 <= value <= 300.0, "Gas level out of range")

    def test_humidity_sensor(self):
        value = self.system.humidity_sensor.read_data()
        self.assertTrue(10.0 <= value <= 90.0, "Humidity out of range")

    def test_evaluate_safety_safe(self):
        data = {"temperature": 30.0, "gas_level": 100.0, "humidity": 50.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "SAFE", "System should be safe")

    def test_evaluate_safety_high_temperature(self):
        data = {"temperature": 50.1, "gas_level": 100.0, "humidity": 50.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: High Temperature", "Failed to detect high temperature")

    def test_evaluate_safety_high_gas(self):
        data = {"temperature": 30.0, "gas_level": 200.1, "humidity": 50.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: High Gas Levels", "Failed to detect high gas levels")

    def test_evaluate_safety_low_humidity(self):
        data = {"temperature": 30.0, "gas_level": 100.0, "humidity": 19.9}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: Unsafe Humidity", "Failed to detect low humidity")

    def test_evaluate_safety_high_humidity(self):
        data = {"temperature": 30.0, "gas_level": 100.0, "humidity": 80.1}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: Unsafe Humidity", "Failed to detect high humidity")

    def test_log_data(self):
        data = {"temperature": 45.0, "gas_level": 150.0, "humidity": 55.0}
        self.system.log_data(data)
        with open("sensor_log.csv", "r") as log_file:
            logs = log_file.readlines()
        self.assertIn("45.00", logs[-1], "Log entry missing temperature")
        self.assertIn("150.00", logs[-1], "Log entry missing gas level")
        self.assertIn("55.00", logs[-1], "Log entry missing humidity")

    def test_alert_system(self):
        self.system.alert_system.add_alert("Test Alert")
        self.system.alert_system.save_alerts()
        with open("alerts_log.txt", "r") as alert_file:
            alerts = alert_file.readlines()
        self.assertIn("Test Alert", alerts[-1], "Alert system failed to save alerts")


if __name__ == "__main__":
    unittest.main()
