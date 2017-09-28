from unittest import TestCase
from jenduino.arduino_connection import ArduinoConnection


class ArduinoConnectionTest(TestCase):
    def test_convert_data(self):
        connection = ArduinoConnection('COM3', 8000)

        test_data = [{'id': 'job1',
                      'status': 'blue'}]

        result_bytes = connection.convert_data(test_data)

        expected_bytes = [0xe0, 0xFF]
        self.assertEqual(expected_bytes, result_bytes)
