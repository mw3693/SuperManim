# File location: /home/mina/SuperManim/core/entities/audio_settings.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class AudioSettings:
    """
    AudioSettings stores all metadata about the project-level audio file.

    This is a pure data container (entity). It does NOT play, read, or convert
    audio. It only describes the master audio file (narration or background music)
    that spans the entire project.

    Main fields:
        - audio_format: format of the audio file (mp3, wav, etc.)
        - audio_file_path: path to the audio file on disk
        - audio_total_duration: total duration in milliseconds

    Optional fields (enhanced metadata):
        - audio_sample_rate: samples per second (Hz)
        - audio_channels: number of audio channels (mono/stereo)
        - audio_bit_depth: bits per audio sample
        - audio_bitrate: bits per second for compressed audio
        - is_audio_exist: whether audio is present
        - audio_file_size_byte: size of the audio file in bytes
    """

    # === MAIN PROPERTIES ===
    # The audio file format (lowercase string)
    # Examples: "mp3", "wav", "ogg", "aac", "flac", "m4a"
    audio_format: str = "mp3"

    # Full path to the master audio file (relative or absolute)
    audio_file_path: str = ""

    # Total duration of the audio in milliseconds
    audio_total_duration: int = 0

    # True if the audio file exists in the project
    is_audio_exist: bool = False

    # Size of the audio file in bytes
    audio_file_size_byte: int = 0

    # === OPTIONAL PROPERTIES ===
    # Number of audio samples per second in Hertz
    # Common: 44100, 48000, 96000
    audio_sample_rate: Optional[int] = 44100

    # Number of channels: 1 = mono, 2 = stereo
    audio_channels: Optional[int] = 1

    # Bits per audio sample: 16, 24, 32
    audio_bit_depth: Optional[int] = 16

    # Audio bitrate (optional, only for compressed formats like mp3 or aac)
    # Example: 128000, 192000, 320000
    audio_bitrate: Optional[int] = None
