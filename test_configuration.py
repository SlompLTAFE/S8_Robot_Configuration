# test_configuration.py — fill in the test bodies
import unittest
import os
import json

from configuration_manager import (
    ConfigurationManager,
    ConfigNotFoundError,
    ConfigParseError,
    ConfigValidationError
)


class TestConfigurationManagerLoad(unittest.TestCase):

    def setUp(self):
        """Create a minimal valid config file for use in tests."""
        self.valid_file = 'test_valid_config.json'

        with open(self.valid_file, 'w') as f:
            json.dump({
                'robot_id': 'test_robot',
                'robot_type': 'cleaning',
                'name': 'Test Robot',
                'battery_level': 100,
                'is_moving': False,
                'sensor_reading': 25
            }, f)

    def tearDown(self):
        """Remove test files created during tests."""
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)

    def test_load_valid_json(self):
        """ConfigurationManager loads a valid JSON file without error."""
        config = ConfigurationManager(self.valid_file)

        self.assertEqual(config.get('robot_id'), 'test_robot')
        self.assertEqual(config.get('battery_level'), 100)

    def test_load_missing_file_raises_error(self):
        """ConfigNotFoundError is raised when file does not exist."""
        with self.assertRaises(ConfigNotFoundError):
            ConfigurationManager('missing_config.json')

    def test_load_corrupted_file_raises_error(self):
        """ConfigParseError is raised when file contains invalid JSON."""
        invalid_file = 'invalid_config.json'

        try:
            with open(invalid_file, 'w') as f:
                f.write('{ invalid json }')

            with self.assertRaises(ConfigParseError):
                ConfigurationManager(invalid_file)

        finally:
            if os.path.exists(invalid_file):
                os.remove(invalid_file)


class TestConfigurationManagerGet(unittest.TestCase):

    def setUp(self):
        self.valid_file = 'test_get_config.json'

        with open(self.valid_file, 'w') as f:
            json.dump({
                'robot_id': 'test_robot',
                'sensors': {
                    'ir_count': 4,
                    'threshold': 0.5
                }
            }, f)

        self.config = ConfigurationManager(self.valid_file)

    def tearDown(self):
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)

    def test_get_simple_key(self):
        """get() returns correct value for a top-level key."""
        self.assertEqual(
            self.config.get('robot_id'),
            'test_robot'
        )

    def test_get_nested_key_dot_notation(self):
        """get() returns correct value for a nested key using dot notation."""
        self.assertEqual(
            self.config.get('sensors.ir_count'),
            4
        )

    def test_get_missing_key_returns_default(self):
        """get() returns the provided default when key does not exist."""
        self.assertEqual(
            self.config.get('missing_key', 'default_value'),
            'default_value'
        )


class TestConfigurationManagerValidate(unittest.TestCase):

    def setUp(self):
        self.valid_file = 'test_validate_config.json'

        with open(self.valid_file, 'w') as f:
            json.dump({
                'robot_id': 'test_robot',
                'robot_type': 'cleaning',
                'name': 'Test Robot',
                'battery_level': 100,
                'is_moving': False,
                'sensor_reading': 25
            }, f)

        self.config = ConfigurationManager(self.valid_file)

    def tearDown(self):
        if os.path.exists(self.valid_file):
            os.remove(self.valid_file)

    def test_valid_config_passes_validation(self):
        """validate() does not raise when config data is valid."""
        self.assertTrue(self.config.validate())

    def test_missing_required_field_raises_validation_error(self):
        """ConfigValidationError is raised when a required field is absent."""
        del self.config.config['name']

        with self.assertRaises(ConfigValidationError):
            self.config.validate()

    def test_invalid_field_type_raises_validation_error(self):
        """ConfigValidationError is raised when a field has the wrong type."""
        self.config.config['battery_level'] = 'full'

        with self.assertRaises(ConfigValidationError):
            self.config.validate()


if __name__ == '__main__':
    unittest.main()