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

from robot_base import CleaningRobot, SecurityRobot, DeliveryRobot


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

                self.config = {}

                for child in root:
                    value = child.text

                    if value is None:
                        value = ""

                    elif value.lower() == "true":
                        value = True

                    elif value.lower() == "false":
                        value = False

                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value) # Just in case for if int values are not suitable for newer changes to Robots.
                            except ValueError:
                                pass

                    self.config[child.tag] = value

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
    
    def validate(self):
        """
        Validate the loaded robot configuration.

        Raises:
            ConfigValidationError: If the configuration contains invalid data.
        """
        errors = []

        required_fields = [
            "robot_id",
            "robot_type",
            "name",
            "battery_level",
            "is_moving",
            "sensor_reading"
        ]

        for field in required_fields:
            if field not in self.config:
                errors.append(f"Missing required field: {field}")

        if "battery_level" in self.config:
            battery_level = self.config["battery_level"]

            if not isinstance(battery_level, (int, float)):
                errors.append("Battery must be higher!.")
            elif not 0 <= battery_level <= 100:
                errors.append("Battery level must be between 0 and 100!")

        if "is_moving" in self.config:
            if not isinstance(self.config["is_moving"], bool):
                errors.append("is_moving must be a Boolean True or False.")

        if errors:
            raise ConfigValidationError(errors)

        return True
    
    def create_robot(self):
        """
        Create a robot object based on the loaded configuration.

        Returns:
            A robot object matching the configured robot type.

        Raises:
            ConfigValidationError: If the configuration is invalid.
            ConfigurationError: If the robot type is unsupported.
        """
        self.validate()

        robot_type = self.config["robot_type"]

        robot_classes = {"cleaning": CleaningRobot, "security": SecurityRobot, "delivery": DeliveryRobot}

        if robot_type not in robot_classes:
            raise ConfigurationError(f"Unsupported robot type: {robot_type}")

        robot_class = robot_classes[robot_type]

        return robot_class(
            self.config["name"],
            self.config["battery_level"],
            self.config["is_moving"],
            self.config["sensor_reading"]
        )
    
    def save(self):
        """
        Save the current configuration back to the configuration file.

        The file format is detected from the file extension.
        """

        file_extension = os.path.splitext(self.config_file)[1].lower()

        try:
            if file_extension == ".json":
                with open(self.config_file, "w") as file:
                    json.dump(self.config, file, indent=4)

            elif file_extension == ".xml":
                root = ET.Element("robot")

                for key, value in self.config.items():
                    child = ET.SubElement(root, key)
                    child.text = str(value)

                tree = ET.ElementTree(root)
                ET.indent(tree, space="    ")
                tree.write(
                    self.config_file,
                    encoding="utf-8",
                    xml_declaration=True
                )

            else:
                raise ConfigParseError(
                    self.config_file,
                    f"Unsupported file format: {file_extension}"
                )

        except OSError as error:
            raise ConfigurationError(
                f"Error saving configuration file {self.config_file}: {error}"
            ) from error
            


print("JSON robot:")
json_config = ConfigurationManager("example_config.json")
json_robot = json_config.create_robot()
print(type(json_robot).__name__)
json_robot.perform_task()

print("\nXML robot:")
xml_config = ConfigurationManager("example_config.xml")
xml_robot = xml_config.create_robot()
print(type(xml_robot).__name__)
xml_robot.perform_task()