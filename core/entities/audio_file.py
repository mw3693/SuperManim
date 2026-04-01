# File location: /home/mina/SuperManim/core/entities/audio_file.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class AudioFile:
    """
    The AudioFile Entity represents the master audio file added to the project.

    It is a pure data container. It holds metadata about the original
    full-length audio file — its path, format, duration, and technical
    properties. It also holds references to all the AudioClip objects
    that were cut from it.

    It does NOT read audio files. It does NOT call FFmpeg.
    It is just structured data.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    audio_file_id:              int

    # ── GROUP 2 — LOCATION ────────────────────────────────────────────
    audio_file_path:            Optional[str]   = None
    audio_file_original_name:   Optional[str]   = None

    # ── GROUP 3 — FORMAT ──────────────────────────────────────────────
    audio_file_format:          str             = "mp3"

    # ── GROUP 4 — TIMING ──────────────────────────────────────────────
    audio_file_duration:        Optional[float] = None

    # ── GROUP 5 — TECHNICAL PROPERTIES ───────────────────────────────
    audio_file_sample_rate:     Optional[int]   = None
    audio_file_channels:        int             = 1
    audio_file_bitrate:         Optional[int]   = None
    audio_file_size_bytes:      Optional[int]   = None

    # ── GROUP 6 — CLIPS ───────────────────────────────────────────────
    audio_clips:                List            = field(default_factory=list)

    # ── GROUP 7 — STATE ───────────────────────────────────────────────
    audio_file_is_split:        bool            = False
      
