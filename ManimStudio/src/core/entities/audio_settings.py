# core/entities/audio_settings.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from constants import (
    DEFAULT_AUDIO_FORMAT,
    DEFAULT_AUDIO_SAMPLE_RATE,
    DEFAULT_AUDIO_CHANNEL,
    DEFAULT_AUDIO_BITRATE,
)

@dataclass(slots=True, kw_only=True)
class AudioSettings:
    """
    AudioSettings stores all metadata about the project-level audio file.

    Fields with defaults are applied immediately on creation.
    audio_bit_depth is Optional because lossy formats (mp3, aac, opus …)
    have no fixed bit depth — only uncompressed formats (wav, aiff …) do.
    """

    # The audio file format (e.g., "mp3", "wav")
    audio_format: str = DEFAULT_AUDIO_FORMAT

    # Samples per second (Hz)
    audio_sample_rate: int = DEFAULT_AUDIO_SAMPLE_RATE

    # 1 = mono, 2 = stereo
    audio_channels: int = DEFAULT_AUDIO_CHANNEL

    # Audio bitrate (bps)
    audio_bitrate: int = DEFAULT_AUDIO_BITRATE

    # Bits per audio sample.
    # None for lossy formats (mp3, aac …) — only set for uncompressed ones (wav, aiff …).
    audio_bit_depth: Optional[int] = None
