from abc import ABC, abstractmethod


class RobotBase(ABC):
    def __init__(self, name, battery_level, is_moving, sensor_reading):
        """Initialize the robot base with the given parameters: 
        Args:
            name: The name of the robot
            battery_level: The current battery level of the robot
            is_moving: A boolean indicating if the robot is currently moving
            sensor_reading: The latest reading from the robot's sensor
        """
        self._name = name
        self._battery_level = battery_level
        self._is_moving = is_moving
        self._sensor_reading = sensor_reading
        
    @property
    def name(self):
        """Get the name of the robot."""
        return self._name

    @property
    def battery_level(self):
        """Get the battery level of the robot."""
        return self._battery_level

    @property
    def is_moving(self):
        """Get the moving status of the robot."""
        return self._is_moving

    @property
    def sensor_reading(self):
        """Get the latest sensor reading of the robot."""
        return self._sensor_reading
    
    @battery_level.setter
    def battery_level(self, value):
        """Sets the battery level."""
        if 0 <= value <= 100:
            self._battery_level = value
        else:
            raise ValueError("Battery level must be between 0 and 100.")
    @abstractmethod  
    def perform_task(self):
        """Perform the specialized task of the robot."""
        pass 
    def move_forward(self, speed: int):
        """Move the robot forward at the specified speed."""
        if not self._is_moving:
            self._is_moving = True
        
    def stop(self):
        """Stop the robot's movement."""
        if self._is_moving:
            self._is_moving = False
    
    def get_sensor_reading(self):
        """Return the latest sensor reading."""
        return self._sensor_reading
    
    def set_sensor_reading(self, reading):
        """Set a new sensor reading."""
        self._sensor_reading = reading
        
    def report_status(self):
        """Report the Robot's status via it's private attributes."""
        status = {f"Robot Name:{self._name} | "
                  f"Battery Level:{self._battery_level} | "
                  f"Is Moving:{self._is_moving} | "
                  f"Sensor Reading:{self._sensor_reading}"
                  }
        return status
    
    def __str__(self):
        """Return a user-friendly string of the Robot's status for users."""
        return (f"Robot Name: {self._name}, "
                f"Battery Level: {self._battery_level}")
        
    def __repr__(self):
        """Return a developer-friendly string of the Robot's status for debugging."""
        return (f"RobotBase(name={self._name!r}, "
                f"battery_level={self._battery_level!r}, "
                f"is_moving={self._is_moving!r}, "
                f"sensor_reading={self._sensor_reading!r})")
class CleaningRobot(RobotBase):
    """Represents a robot designed to do cleaning tasks."""

    def __init__(self, name, battery_level, is_moving, sensor_reading):
        """Initialize a cleaning robot.

        Args:
            name: The name of the robot.
            battery_level: The current battery level of the robot.
            is_moving: Whether the robot is currently moving.
            sensor_reading: The latest reading from the robot's sensor.
        """
        super().__init__(name, battery_level, is_moving, sensor_reading)

    def perform_task(self):
        """Perform the cleaning robot's specialized task."""
        print(f"{self.name} is cleaning.")
        
class SecurityRobot(RobotBase):
    """Represents a robot designed to do security tasks."""

    def __init__(self, name, battery_level, is_moving, sensor_reading):
        """Initialize a security robot.

        Args:
            name: The name of the robot.
            battery_level: The current battery level of the robot.
            is_moving: Whether the robot is currently moving.
            sensor_reading: The latest reading from the robot's sensor.
        """
        super().__init__(name, battery_level, is_moving, sensor_reading)

    def perform_task(self):
        """Perform the security robot's specialized task."""
        print(f"{self.name} is patrolling the area.")
        
class DeliveryRobot(RobotBase):
    """Represents a robot designed to do delivery tasks."""

    def __init__(self, name, battery_level, is_moving, sensor_reading):
        """Initialize a delivery robot.

        Args:
            name: The name of the robot.
            battery_level: The current battery level of the robot.
            is_moving: Whether the robot is currently moving.
            sensor_reading: The latest reading from the robot's sensor.
        """
        super().__init__(name, battery_level, is_moving, sensor_reading)

    def perform_task(self):
        """Perform the delivery robot's specialized task."""
        print(f"{self.name} is delivering a package.")
        
        
def run_robot_task(robot: RobotBase):
    """Run the task for a robot.

    Args:
        robot: A robot that inherited from RobotBase.
    """
    robot.perform_task()
    
    
# Example Here, used to test Polymorphism with Inheritance via using the base class alongside perform_task.
cleaner = CleaningRobot("Dusty", 80, False, 25)
security = SecurityRobot("Guard", 90, False, 30)
delivery = DeliveryRobot("Courier", 70, False, 15)

run_robot_task(cleaner)
run_robot_task(security)
run_robot_task(delivery)