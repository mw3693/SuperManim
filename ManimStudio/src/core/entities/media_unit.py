# Location: SuperManim/src/core/entities/media_unit.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass(slots=True)
class MediaUnit:
    """
    Represents a single unit or clip of a media file.

    This class is meant to be a base for VideoClip and AudioClip entities,
    providing basic timing and metadata information for a segment of a media file.

    Attributes:
        unit_id (int):
            Unique identifier of the unit within its parent media file.

        start_time_ms (int):
            Start time of the unit in milliseconds.

        end_time_ms (int):
            End time of the unit in milliseconds.

        duration_ms (Optional[int]):
            Duration of the unit in milliseconds.
            If not provided, it can be computed as end_time_ms - start_time_ms.

        metadata (Optional[dict]):
            Additional metadata associated with this unit.
            Example: {"scene": 1, "label": "intro"}.
    """

    unit_id        : int                          # The identifer of the child unit
    start_time_ms  : int
    end_time_ms    : int
    unit_path      : Path                         # The location of the unit in the project        

    parent_unit_id : Optional[int] = None         # The identifer of the parent of the child unit        

    @property
    def duration_ms(self) -> float:
         """Returns the duration of the unit in milliseconds."""
         return self.end_time_ms - self.start_time_ms

    
    @property
    def duration_seconds(self) -> float:
        """Returns the duration of the unit in seconds."""
        return self.duration_ms / 1000

    @property
    def start_seconds(self) -> float:
        """Returns the start time in seconds."""
        return self.start_time_ms / 1000

    @property
    def end_seconds(self) -> float:
        """Returns the end time in seconds."""
        return self.end_time_ms / 1000




