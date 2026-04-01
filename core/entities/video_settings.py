# File location: /home/mina/SuperManim/core/entities/video_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoSettings:
    """
    VideoSettings stores all configuration and metadata for video output.
    It describes canvas size, aspect ratio, frame rate, background color, codec,
    file paths, duration, and other key properties needed for rendering animations.

    This entity does not hold video frames or perform rendering.
    It is a pure data container (blueprint) for video creation.
    """

    # === Video Dimensions ===
    video_width: int = 1920
    video_height: int = 1080
    video_aspect_ratio: str = "16:9"

    # === Frame Rate ===
    video_frame_rate: int = 30

    # === Visual Appearance ===
    video_background_color: Optional[str] = "#000000"

    # === Timing ===
    video_total_duration: int = 0.0  # in seconds

    # === Output File ===
    video_file_path: str = None
    video_codec: Optional[str] = "h264"

    # === File Status ===
    is_video_exist: bool = False
    video_file_size_byte: int = 0
