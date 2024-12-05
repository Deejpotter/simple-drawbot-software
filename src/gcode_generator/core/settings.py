"""
Machine Settings Module

This module provides a data class for managing CNC machine settings, particularly
for pen plotter operations. It handles serialization, validation, and persistence
of machine configuration.

References:
    - Python dataclasses: https://docs.python.org/3/library/dataclasses.html
    - Type hints: https://docs.python.org/3/library/typing.html
    - Path handling: https://docs.python.org/3/library/pathlib.html
    - JSON operations: https://docs.python.org/3/library/json.html
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, ClassVar
import json
from pathlib import Path
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class MachineSettings:
    """
    Represents CNC machine settings for pen plotter operations.

    This class uses @dataclass for automatic generation of special methods
    and provides validation and persistence capabilities.

    Attributes:
        bed_width (float): Width of the machine bed in millimeters
        bed_height (float): Height of the machine bed in millimeters
        feed_rate (float): Speed of movement in mm/minute
        pen_up_position (float): Z-axis position when pen is raised
        pen_down_position (float): Z-axis position when pen is lowered
        safe_z (float): Safe Z-axis travel height for movements

    Example:
        >>> settings = MachineSettings()  # Creates with default values
        >>> settings.save('machine_config.json')  # Saves to file
        >>> loaded = MachineSettings.load('machine_config.json')  # Loads from file
    """

    # Class constants for validation
    MIN_DIMENSION: ClassVar[float] = 0.1
    MAX_DIMENSION: ClassVar[float] = 1000.0
    MIN_FEED_RATE: ClassVar[float] = 1.0
    MAX_FEED_RATE: ClassVar[float] = 5000.0

    # Instance attributes with default values
    bed_width: float = 200.0
    bed_height: float = 200.0
    feed_rate: float = 1000.0
    pen_up_position: float = 1.0
    pen_down_position: float = 0.0
    safe_z: float = 1.0

    def __post_init__(self) -> None:
        """
        Validates settings after initialization.

        Raises:
            ValueError: If any settings are outside valid ranges or logically inconsistent
        """
        self._validate_dimensions()
        self._validate_feed_rate()
        self._validate_z_positions()

    def _validate_dimensions(self) -> None:
        """Validates bed dimensions are within acceptable ranges."""
        if not self.MIN_DIMENSION <= self.bed_width <= self.MAX_DIMENSION:
            raise ValueError(
                f"Bed width must be between {self.MIN_DIMENSION} and {self.MAX_DIMENSION}mm"
            )
        if not self.MIN_DIMENSION <= self.bed_height <= self.MAX_DIMENSION:
            raise ValueError(
                f"Bed height must be between {self.MIN_DIMENSION} and {self.MAX_DIMENSION}mm"
            )

    def _validate_feed_rate(self) -> None:
        """Validates feed rate is within acceptable range."""
        if not self.MIN_FEED_RATE <= self.feed_rate <= self.MAX_FEED_RATE:
            raise ValueError(
                f"Feed rate must be between {self.MIN_FEED_RATE} and {self.MAX_FEED_RATE}mm/min"
            )

    def _validate_z_positions(self) -> None:
        """Validates Z-axis positions are logically consistent."""
        if self.pen_down_position > self.pen_up_position:
            raise ValueError("Pen down position must be lower than pen up position")
        if self.safe_z < self.pen_up_position:
            raise ValueError("Safe Z must be higher than pen up position")

    def to_dict(self) -> Dict[str, float]:
        """
        Converts settings to a dictionary format.

        Returns:
            Dict[str, float]: Dictionary containing all settings
        """
        return asdict(self)  # Using dataclasses.asdict for reliable conversion

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MachineSettings':
        """
        Creates a MachineSettings instance from a dictionary.

        Args:
            data: Dictionary containing settings values

        Returns:
            MachineSettings: New instance with provided settings

        Raises:
            KeyError: If required settings are missing
            ValueError: If settings values are invalid
        """
        required_keys = {
            'bed_width', 'bed_height', 'feed_rate',
            'pen_up_position', 'pen_down_position', 'safe_z'
        }

        # Check for missing keys
        missing_keys = required_keys - set(data.keys())
        if missing_keys:
            raise KeyError(f"Missing required settings: {missing_keys}")

        # Validate data types
        try:
            return cls(**{k: float(v) for k, v in data.items() if k in required_keys})
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid setting value: {str(e)}")

    def save(self, filepath: str | Path = 'settings.json') -> None:
        """
        Saves settings to a JSON file.

        Args:
            filepath: Path to save the settings file (str or Path object)

        Raises:
            IOError: If file cannot be written
        """
        filepath = Path(filepath)
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with filepath.open('w') as f:
                json.dump(self.to_dict(), f, indent=4)
            logger.info(f"Settings saved to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save settings to {filepath}: {e}")
            raise

    @classmethod
    def load(cls, filepath: str | Path = 'settings.json') -> 'MachineSettings':
        """
        Loads settings from a JSON file.

        Args:
            filepath: Path to the settings file (str or Path object)

        Returns:
            MachineSettings: Instance with loaded settings

        Raises:
            FileNotFoundError: If settings file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
            ValueError: If settings values are invalid
        """
        filepath = Path(filepath)
        try:
            with filepath.open('r') as f:
                data = json.load(f)
            settings = cls.from_dict(data)
            logger.info(f"Settings loaded from {filepath}")
            return settings
        except FileNotFoundError:
            logger.warning(f"Settings file {filepath} not found, using defaults")
            return cls()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in settings file {filepath}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Invalid settings in {filepath}: {e}")
            raise
