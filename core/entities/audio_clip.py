# File location: /home/mina/SuperManim/core/entities/audio_clip.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from core.entities.media_unit import MediaUnit


@dataclass
class AudioClip(MediaUnit):
    """
    The AudioClip Entity represents one cut section of the master audio file.

    It is a pure data container. It holds information about a specific
    audio clip file on disk — its path, its timing, its format, and its
    relationship to a Scene.

    It does NOT call FFmpeg. It does NOT read audio files from disk.
    It does NOT play audio. It does NOT call print(). It is just data.

    TIMING NOTE:
    The timing fields inherited from MediaUnit (start_time, end_time,
    duration) use milliseconds like all other entities.

    The AudioClip-specific timing fields (audio_clip_duration,
    audio_clip_start_time, audio_clip_end_time) store values in
    SECONDS as floats — because this is the native unit used by audio
    file metadata and audio analysis tools like librosa and FFprobe.
    """

    # ── GROUP 1 — IDENTITY ────────────────────────────────────────────
    audio_clip_id:              int             = 0
    audio_file_id:              int             = 0

    # ── GROUP 2 — ORDERING AND LINKING ───────────────────────────────
    audio_clip_index:           int             = 0
    scene_id:                   Optional[int]   = None

    # ── GROUP 3 — LOCATION ────────────────────────────────────────────
    audio_clip_path:            Optional[str]   = None

    # ── GROUP 4 — FORMAT ──────────────────────────────────────────────
    audio_clip_format:          str             = "mp3"

    # ── GROUP 5 — TIMING (in SECONDS as floats — audio convention) ────
    audio_clip_duration:        Optional[float] = None
    audio_clip_start_time:      Optional[float] = None
    audio_clip_end_time:        Optional[float] = None

    # ── GROUP 6 — TECHNICAL PROPERTIES ───────────────────────────────
    audio_clip_sample_rate:     Optional[int]   = None
    audio_clip_channels:        int             = 1
    audio_clip_file_size_bytes: Optional[int]   = None

    # ── GROUP 7 — STATE ───────────────────────────────────────────────
    audio_clip_is_synced:       bool            = False
    audio_clip_created_at:      Optional[str]   = None

    # NOTE: The unit_type field (inherited from MediaUnit) is always
    # set to "audio_clip" for AudioClip instances. It tells the system
    # what type of MediaUnit this is when iterating over project_items.
    # Set it explicitly when creating an AudioClip:
    #   AudioClip(unit_type="audio_clip", audio_clip_id=3, ...)
