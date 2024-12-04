from dataclasses import dataclass
from typing import Dict, Any
import json
import os


@dataclass
class MachineSettings:
    bed_width: float = 200.0
    bed_height: float = 200.0
    feed_rate: float = 1000.0
    pen_up_position: float = 5.0
    pen_down_position: float = 0.0
    safe_z: float = 10.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'bed_width': self.bed_width,
            'bed_height': self.bed_height,
            'feed_rate': self.feed_rate,
            'pen_up_position': self.pen_up_position,
            'pen_down_position': self.pen_down_position,
            'safe_z': self.safe_z
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MachineSettings':
        return cls(**data)

    def save(self, filename: str = 'settings.json'):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load(cls, filename: str = 'settings.json') -> 'MachineSettings':
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
            return cls.from_dict(data)
        return cls()  # Return default settings if file doesn't exist
