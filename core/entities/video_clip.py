# File location: /home/mina/SuperManim/core/entities/video_clip.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from core.entities.media_unit import MediaUnit


@dataclass
class VideoClip(MediaUnit):
    """
    The VideoClip Entity represents one cut section of a master video file.

    It is a pure data container. It holds all the information about a
    specific video clip file on disk — its path, its timing, its
    visual dimensions, its codec, and its link to a Scene.

    It does NOT call FFmpeg. It does NOT read video files.
    It does NOT decode frames. It is just structured data.

    All timing values (video_clip_duration, video_clip_start_time,
    video_clip_end_time) are stored as integers in MILLISECONDS,
    consistent with the rest of the system.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    video_clip_id:              int             = 0
    video_file_id:              int             = 0

    # ── GROUP 2 — ORDERING AND LINKING ───────────────────────────────
    video_clip_index:           int             = 0
    scene_id:                   Optional[int]   = None

    # ── GROUP 3 — LOCATION ────────────────────────────────────────────
    video_clip_path:            Optional[str]   = None

    # ── GROUP 4 — FORMAT ──────────────────────────────────────────────
    video_clip_format:          str             = "mp4"

    # ── GROUP 5 — TIMING (in milliseconds) ────────────────────────────
    video_clip_duration:        Optional[int]   = None
    video_clip_start_time:      Optional[int]   = None
    video_clip_end_time:        Optional[int]   = None

    # ── GROUP 6 — VISUAL PROPERTIES ───────────────────────────────────
    video_clip_resolution:      Optional[str]   = None
    video_clip_fps:             Optional[int]   = None
    video_clip_has_audio:       bool            = False

    # ── GROUP 7 — TECHNICAL PROPERTIES ───────────────────────────────
    video_clip_file_size_bytes: Optional[int]   = None
    video_clip_codec:           Optional[str]   = None

    # ── GROUP 8 — STATE ───────────────────────────────────────────────
    video_clip_status:          str             = "pending"
    video_clip_created_at:      Optional[str]   = None
 
