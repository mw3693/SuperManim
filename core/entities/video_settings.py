from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoSettings:
    """
    VideoSettings defines the visual properties of the project output.
    All fields are Optional and default to None until explicitly set 
    by the user or the rendering engine.
    """

    # --- RESOLUTION & RATIO ---
    
    # Width of the video in pixels (e.g., 1920, 1080, 720)
    video_width: Optional[int] = None

    # Height of the video in pixels (e.g., 1080, 1920, 720)
    video_height: Optional[int] = None


    # --- FRAME RATE & QUALITY ---
    
    # Frames per second (Common: 24, 30, 60)
    # Higher FPS means smoother animation but longer render time
    video_fps: Optional[int] = None

    # Video codec for the final output (e.g., "libx264", "h264")
    video_codec: Optional[str] = None

    # Target video format/extension (e.g., "mp4", "mov")
    video_format: Optional[str] = None
 
