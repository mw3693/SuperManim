# Location supermanim/src/core/entities/audio_file.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List
from src.core.entities.media_file import MediaFile


@dataclass(slots=True)
class AudioFile(MediaFile):
    """
    Represents an audio file, extending MediaFile with audio-specific metadata.

    Attributes:
        sample_rate (int):
            Audio sample rate in Hz (e.g., 44100, 48000).

        channels (int):
            Number of audio channels (1=mono, 2=stereo, etc.).

        audio_codec (str):
            Audio codec used (e.g., 'mp3', 'aac', 'flac').

        bit_depth (Optional[int]):
            Number of bits per sample. Default is None.

        language (Optional[str]):
            Language of the audio track. Default is None.

        album (Optional[str]):
            Album name if available. Default is None.

        artist (Optional[str]):
            Artist name if available. Default is None.

        track_title (Optional[str]):
            Track title if available. Default is None.
    """

    # ------------------- Required Fields -------------------
    sample_rate  : int
    channels     : int
    audio_codec  : str

    # ------------------- Optional Fields -------------------
    bit_depth: Optional[int] = None

    # ------------------- Properties -------------------

    @property
    def duration_seconds(self) -> float:
        """
        Returns the duration of the audio in seconds.
        """
        return self.file_duration_ms / 1000

    @property
    def bitrate_kbps(self) -> Optional[float]:
        """
        Returns the bitrate of the audio in kilobits per second (Kbps).
        Returns None if bitrate is not set.
        """
        if self.bitrate is not None:
            return self.bitrate / 1000
        return None

    @property
    def is_stereo(self) -> bool:
        """
        Returns True if the audio has 2 channels (stereo).
        """
        return self.channels == 2

    @property
    def is_mono(self) -> bool:
        """
        Returns True if the audio has 1 channel (mono).
        """
        return self.channels == 1

    @property
    def sample_rate_khz(self) -> float:
        """
        Returns the sample rate in kHz.
        """
        return self.sample_rate / 1000
