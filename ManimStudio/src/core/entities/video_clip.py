# Location: SuperManim/src/core/entities/video_clip.py
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from src.core.entities.media_unit import MediaUnit


@dataclass(slots=True,  kw_only=True)
class VideoClip(MediaUnit):
    """
    Represents a video segment (clip) derived from a VideoFile.

    Extends MediaUnit with video-specific properties and metadata.

    Attributes:
        width (int):
            Width of the video in pixels.

        height (int):
            Height of the video in pixels.

        fps (int):
            Frames per second.

        video_codec (str):
            Video codec used, e.g., "h264", "vp9".

        color_depth (Optional[int]):
            Bits per color channel.

        rotation (Optional[int]):
            Rotation angle in degrees.

        audio_codec (Optional[str]):
            Audio codec used, if any.

        subtitle_languages (Optional[List[str]]):
            List of available subtitle languages.
    """

    # ------------------- Required Fields -------------------
    width: int
    height: int
    fps: int
    video_codec: str  # unified name

    # ------------------- Optional Fields -------------------
    color_depth: Optional[int] = None
    rotation: Optional[int] = None
    audio_codec: Optional[str] = None
    subtitle_languages: List[str] = field(default_factory=list)
    bitrate: Optional[int] = None
    # ------------------- Properties -------------------

    @property
    def aspect_ratio(self) -> float:
        """Returns the aspect ratio (width / height) of the video."""
        return self.width / self.height

    @property
    def bitrate_kbps(self) -> Optional[float]:
        """Returns the bitrate of the video in kilobits per second (Kbps)."""
        if self.bitrate is not None:
            return self.bitrate / 1000
        return None

    @property
    def resolution(self) -> str:
        """Returns the video resolution as 'widthxheight'."""
        return f"{self.width}x{self.height}"

    @property
    def is_landscape(self) -> bool:
        """Returns True if the video is wider than it is tall."""
        return self.width >= self.height

    @property
    def is_portrait(self) -> bool:
        """Returns True if the video is taller than it is wide."""
        return self.height > self.width

    @property
    def fps_str(self) -> str:
        """Returns FPS as a string with 'fps' unit."""
        return f"{self.fps} fps"

    @property
    def has_subtitles(self) -> bool:
        """Returns True if subtitles are available."""
        return bool(self.subtitle_languages)
