class ConfigurationError(Exception): 
    """
    The Base Error when finding exceptions in configuration.
    """
    pass

class ConfigNotFoundError(ConfigurationError):
    """
    Raised when a configuration file is not found.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__(f"Configuration file not found: {file_path}")
        
class ConfigParseError(ConfigurationError):
    """
    Raised when a configuration file cannot be parsed.
    """
    def __init__(self, file_path, error_message):
        self.file_path = file_path
        self.error_message = error_message
        super().__init__(f"Error parsing configuration file {file_path}: {error_message}")
        
class ConfigValidationError(ConfigurationError):
    """
    Raised when configuration data fails validation.
    """

    def __init__(self, errors):
        self.errors = errors
        error_list = "\n  - ".join(errors)
        super().__init__(
            f"Configuration validation failed:\n  - {error_list}"
        )
        
import json
import os
import xml.etree.ElementTree as ET


class ConfigurationManager:
    """
    Manages robot configuration files.
    """

    def __init__(self, config_file):
        """Initialize the ConfigurationManager.

        Args:
            config_file: Path to the configuration file.
        """
        self.config_file = config_file
        self.config = {}
        self.load()

    def load(self):
        """
        Load configuration data based on the file extension.
        """

        if not os.path.exists(self.config_file):
            raise ConfigNotFoundError(self.config_file)

        file_extension = os.path.splitext(self.config_file)[1].lower()

        try:
            if file_extension == ".json":
                with open(self.config_file, "r") as file:
                    self.config = json.load(file)

            elif file_extension == ".xml":
                tree = ET.parse(self.config_file)
                root = tree.getroot()

                self.config = {
                    child.tag: child.text
                    for child in root
                }

            else:
                raise ConfigParseError(
                    self.config_file,
                    f"Unsupported file format: {file_extension}"
                )

        except (json.JSONDecodeError, ET.ParseError) as error:
            raise ConfigParseError(
                self.config_file,
                str(error)
            ) from error
    
    def get(self, key, default=None):
        """
        Get a configuration value by key.

        Supports nested keys using dot notation.

        Args:
            key: The configuration key to retrieve.
            default: The default value if the key is not found.

        Returns:
            The configuration value or the default.
        """
        current = self.config

        for part in key.split("."):
            if not isinstance(current, dict) or part not in current:
                return default

            current = current[part]

        return current
            

json_config = ConfigurationManager("example_config.json")
xml_config = ConfigurationManager("example_config.xml")

json_config.config["robot"] = {
    "name": "Duster",
    "battery_level": 80
}

print("JSON:")
print(json_config.get("robot.name"))
print(json_config.get("robot.battery_level"))
print(json_config.get("robot.robot_type"))
print(json_config.get("does_not_exist", "Default Value"))

print("\nXML:")
print(xml_config.get("name"))
print(xml_config.get("battery_level"))
print(xml_config.get("robot_type"))