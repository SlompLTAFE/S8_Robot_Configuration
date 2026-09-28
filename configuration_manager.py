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