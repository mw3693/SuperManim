# Location SuperManim/src/core/entities/video_file.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List
from src.core.entities.media_file import MediaFile


@dataclass(slots=True)
class VideoFile(MediaFile):
    """
    Represents a video file, extending MediaFile with video-specific metadata.

    Attributes:
        width (int):
            Width of the video in pixels.

        height (int):
            Height of the video in pixels.

        fps (int):
            Frames per second of the video.

        codes (str):
            Video codec information (e.g., "h264", "vp9").

        color_depth (Optional[int]):
            Number of bits per color channel. Default is None.

        rotation (Optional[int]):
            Rotation angle in degrees (for mobile/oriented videos). Default is None.

        audio_codec (Optional[str]):
            Audio codec used in the video, if any. Default is None.

        subtitle_languages (Optional[List[str]]):
            List of available subtitle languages. Default is None.
    """

    # ------------------- Required Fields -------------------
    width: int
    height: int
    fps: int
    codec: str

    # ------------------- Optional Fields -------------------
    color_depth: Optional[int] = None
    rotation: Optional[int] = None
    audio_codec: Optional[str] = None
    subtitle_languages: Optional[List[str]] = None

    # ------------------- Properties -------------------

    @property
    def aspect_ratio(self) -> float:
        """
        Returns the aspect ratio (width / height) of the video.
        """
        return self.width / self.height

    @property
    def duration_seconds(self) -> float:
        """
        Returns the duration of the video in seconds.
        """
        return self.file_duration_ms / 1000

    @property
    def bitrate_kbps(self) -> Optional[float]:
        """
        Returns the bitrate of the video in kilobits per second (Kbps).
        Returns None if bitrate is not set.
        """
        if self.bitrate is not None:
            return self.bitrate / 1000
        return None

    @property
    def resolution(self) -> str:
        """
        Returns the video resolution as 'widthxheight'.
        """
        return f"{self.width}x{self.height}"

    @property
    def is_landscape(self) -> bool:
        """
        Returns True if the video is wider than it is tall.
        """
        return self.width >= self.height

    @property
    def is_portrait(self) -> bool:
        """
        Returns True if the video is taller than it is wide.
        """
        return self.height > self.width

    @property
    def fps_str(self) -> str:
        """
        Returns FPS as a string with 'fps' unit.
        """
        return f"{self.fps} fps"

    @property
    def has_subtitles(self) -> bool:
        """
        Returns True if subtitles are available.
        """
        return bool(self.subtitle_languages)

