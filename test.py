import unittest
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
        data = {"temperature": 55.0, "gas_level": 100.0, "humidity": 50.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: High Temperature", "System failed to detect high temperature")

    def test_evaluate_safety_high_gas(self):
        data = {"temperature": 30.0, "gas_level": 250.0, "humidity": 50.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: High Gas Levels", "System failed to detect high gas levels")

    def test_evaluate_safety_unsafe_humidity_low(self):
        data = {"temperature": 30.0, "gas_level": 100.0, "humidity": 10.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: Unsafe Humidity", "System failed to detect low humidity")

    def test_evaluate_safety_unsafe_humidity_high(self):
        data = {"temperature": 30.0, "gas_level": 100.0, "humidity": 85.0}
        status = self.system.evaluate_safety(data)
        self.assertEqual(status, "ALERT: Unsafe Humidity", "System failed to detect high humidity")

if __name__ == "__main__":
    unittest.main()
