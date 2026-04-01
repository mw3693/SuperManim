# File location: /home/mina/SuperManim/core/entities/media_unit.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from abc import ABC


@dataclass
class MediaUnit(ABC):
    """
    MediaUnit is the abstract base class for all media items that
    can appear on a SuperManim project timeline.

    Every concrete media item (AudioClip, VideoClip, Scene) inherits
    from this class and is guaranteed to have a file path, a start time,
    an end time, and a duration.

    This class is abstract — you cannot create a MediaUnit directly.
    You create an AudioClip or a VideoClip or a Scene (which all extend
    this class).

    All timing values are in milliseconds as integers.
    """

    # ── CORE IDENTITY ─────────────────────────────────────────────────
    unit_type:          str                 # "audio_clip", "video_clip", "scene"

    # ── FILE LOCATION ─────────────────────────────────────────────────
    file_path:          Optional[str]       = None

    # ── TIMING (in milliseconds) ───────────────────────────────────────
    start_time:         Optional[int]       = None
    end_time:           Optional[int]       = None
    duration:           Optional[int]       = None
