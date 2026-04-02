from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class Scene:

    start_time        : int
    end_time         : int
    code_path      : Path  # in milliseconds
    bitrate: Optional[int] = None

    # ------------------- Properties -------------------

    @property
    def file_name(self) -> str:
        """
        Returns the file name with extension.
        """
        return self.file_path.name

    @property
    def file_format(self) -> str:
        """
        Returns the file format (extension) in lowercase without the leading dot.
        """
        return self.file_path.suffix[1:] if self.file_path.suffix else ""

    @property
    def duration_seconds(self) -> float:
        """
        Returns the duration of the media file in seconds.
        """
        return self.file_duration_ms / 1000

    @property
    def bitrate_kbps(self) -> Optional[float]:
        """
        Returns the bitrate in kilobits per second (Kbps).
        Returns None if bitrate is not set.
        """
        if self.bitrate is not None:
            return self.bitrate / 1000
        return None

    @property
    def path_str(self) -> str:
        """
        Returns the file path as a string.
        """
        return str(self.file_path)
