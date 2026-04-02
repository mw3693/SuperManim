# Location SuperManim/src/core/entities/media_file.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from src.core.entities.media_unit import MediaUnit

@dataclass(slots=True)
class MediaFile:
    """
    Represents a media file (audio or video) and its associated metadata.

    This entity acts as a lightweight, immutable-style container for file-related
    information used throughout the system.

    Attributes:
        file_path (Path):
            Absolute or relative path to the media file.

        file_size_bytes (int):
            Size of the file in bytes.

        file_duration_ms (int):
            Duration of the media file in milliseconds.

        bitrate (Optional[int]):
            Bitrate of the media file in bits per second (bps).
            May be None if unknown or not applicable.
    """

    file_path       : Path
    file_id         : int
    file_size_bytes : int
    file_duration_ms: int  # in milliseconds
    bitrate         : Optional[int]       = None
    media_unit_list : List[MediaUnit] = field(default_factory=list)
    @property
    def file_name(self) -> str:
        """
        Returns the file name with extension.

        Example:
            "video.mp4"
        """
        return self.file_path.name

    @property
    def file_format(self) -> str:
        """
        Returns the file format (extension) in lowercase without the leading dot.

        Example:
            "mp4", "mp3", "wav"

        Notes:
            - Assumes the file has a valid extension.
            - Does not validate against supported formats.
        """
        return self.file_path.suffix[1:].lower()
