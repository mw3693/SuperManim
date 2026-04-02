from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pathlib import Path
@dataclass
class AudioSettings:
    """
    AudioSettings stores all metadata about the project-level audio file.
    Everything is Optional until the audio file is actually probed/analyzed.
    """

    # === MAIN PROPERTIES ===
    
    # The audio file format (e.g., "mp3", "wav") - None means not set yet
    audio_format: Optional[str] = None

    # Full path to the audio file on disk - Empty or None means no file linked
    audio_file_path: Optional[Path] = None

    # Total duration in milliseconds - 0 or None means unknown duration
    audio_total_duration: Optional[int] = None

    # Size of the audio file in bytes
    audio_file_size_byte: Optional[int] = None

    # === TECHNICAL METADATA (Strictly Optional) ===
    
    # Samples per second (Hz) - Should be None until detected
    audio_sample_rate: Optional[int] = None

    # 1 = mono, 2 = stereo - Should be None until detected
    audio_channels: Optional[int] = None

    # Bits per audio sample - Should be None until detected
    audio_bit_depth: Optional[int] = None

    # Audio bitrate (bps) - Should be None until detected
    audio_bitrate: Optional[int] = None
