# core/entities/video_settings.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from constants import (
    DEFAULT_VIDEO_WIDTH,
    DEFAULT_VIDEO_HEIGHT,
    DEFAULT_FPS,
    DEFAULT_VIDEO_CODEC,
    DEFAULT_VIDEO_FORMAT,
    DEFAULT_VIDEO_BITRATE,
)


@dataclass(slots=True, kw_only=True)
class VideoSettings:
    """
    VideoSettings defines the visual properties of the project output.
    All fields are Optional and default to None until explicitly set 
    by the user or the rendering engine.
    """

    # --- RESOLUTION & RATIO ---

    # Width of the video in pixels (e.g., 1920, 1080, 720)
    video_width: int = DEFAULT_VIDEO_WIDTH

    # Height of the video in pixels (e.g., 1080, 1920, 720)
    video_height: int = DEFAULT_VIDEO_HEIGHT

    # --- FRAME RATE & QUALITY ---

    # Frames per second (Common: 24, 30, 60)
    # Higher FPS means smoother animation but longer render time
    video_fps: Optional[int] = DEFAULT_FPS

    # Video codec for the final output (e.g., "libx264", "h264")
    video_codec: Optional[str] = DEFAULT_VIDEO_CODEC

    # Target video format/extension (e.g., "mp4", "mov")
    video_format: Optional[str] = DEFAULT_VIDEO_FORMAT

    video_bitrate: Optional[int] = DEFAULT_VIDEO_BITRATE
