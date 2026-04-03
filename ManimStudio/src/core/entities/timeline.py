# Location: SuperManim/src/core/entities/timeline.py

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List
from src.core.entities.scene import Scene

class TimelineMode(Enum):
    DYNAMIC = auto()  # Scenario 1: Growth based on scene durations
    FIXED   = auto()  # Scenario 2: Locked to a reference (e.g., Audio)

@dataclass(slots=True, kw_only=True)
class Timeline:
    """
    Pure data container for the Timeline.
    The order is implicitly handled by each Scene's index.
    """

    id: int
    
    # The Master Clock: 
    # In DYNAMIC: The cumulative sum of scenes.
    # In FIXED  : The locked duration from the audio file.
    total_duration_ms: int = 0
    
    # Mode to toggle between Fixed (Audio-based) and Dynamic (Scene-based)
    mode: TimelineMode = TimelineMode.DYNAMIC
    
    # The only source of scenes. Sorting happens via scene_index during processing.
    scenes_list: List[Scene] = field(default_factory=list)

    # ------------------- Metadata Properties (Read-Only) -------------------

    @property
    def scene_count(self) -> int:
        """Returns the total number of scenes currently registered."""
        return len(self.scenes_list)

    @property
    def is_fixed(self) -> bool:
        """Helper to check if the timeline is locked to a fixed duration."""
        return self.mode == TimelineMode.FIXED
