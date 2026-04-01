# File location: /home/mina/SuperManim/core/entities/video_file.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class VideoFile:
    """
    The VideoFile Entity represents a master video file added to the project.

    It is a pure data container. It holds metadata about the original
    full-length video file — its path, format, duration, and technical
    visual properties. It also holds references to all VideoClip objects
    that were cut from it.

    It does NOT read video files. It does NOT call FFmpeg.
    It is just structured data.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    video_file_id:              int

    # ── GROUP 2 — LOCATION ────────────────────────────────────────────
    video_file_path:            Optional[str]   = None
    video_file_original_name:   Optional[str]   = None

    # ── GROUP 3 — FORMAT ──────────────────────────────────────────────
    video_file_format:          str             = "mp4"
    video_file_codec:           Optional[str]   = None

    # ── GROUP 4 — TIMING (in milliseconds) ────────────────────────────
    video_file_duration:        Optional[int]   = None

    # ── GROUP 5 — VISUAL PROPERTIES ───────────────────────────────────
    video_file_resolution:      Optional[str]   = None
    video_file_fps:             Optional[int]   = None
    video_file_has_audio:       bool            = False

    # ── GROUP 6 — TECHNICAL PROPERTIES ───────────────────────────────
    video_file_size_bytes:      Optional[int]   = None
    video_file_bitrate:         Optional[int]   = None

    # ── GROUP 7 — CLIPS ───────────────────────────────────────────────
    video_clips:                List            = field(default_factory=list)

    # ── GROUP 8 — STATE ───────────────────────────────────────────────
    video_file_is_split:        bool            = False
    
