# Location: SuperManim/src/core/entities/scene_audio.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from enum import Enum
from src.core.entities.media_unit import MediaUnit


class AudioFormat(Enum):
    """
    Enum representing supported audio file formats.

    - MP3
    - WAV
    - OGG
    """
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"


@dataclass(slots=True, kw_only=True)
class SceneAudio(MediaUnit):
    """
    Entity representing audio for a specific scene.

    Holds metadata about the audio file, including format, codec,
    channels, sample rate, bit depth, optional transcript, and file hash.

    Attributes
    ----------
    scene_id : int
        Unique identifier of the scene this audio belongs to.
    audio_format : AudioFormat
        Enum representing the audio format.
    file_hash : Optional[str]
        Optional hash of the audio file for validation or caching.
    transcript : Optional[str]
        Optional textual transcript of the audio content.
    sample_rate : Optional[int]
        Audio sample rate in Hz.
    channels : Optional[int]
        Number of channels (1 = mono, 2 = stereo).
    audio_codec : Optional[str]
        Codec used to encode the audio file.
    bit_depth : Optional[int]
        Bit depth of the audio file.
    """

    scene_id: int
    audio_format: AudioFormat
    file_hash: Optional[str] = None
    transcript: Optional[str] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    audio_codec: Optional[str] = None
    bit_depth: Optional[int] = None

    # ------------------- Properties (metadata only) -------------------

    @property
    def scene_audio_filename(self) -> str:
        """
        Returns a standardized filename for the scene audio.

        Example:
            scene_id = 1, audio_format = MP3
            → "scene_audio_01.mp3"
        """
        return f"scene_audio_{self.scene_id:02d}.{self.audio_format.value}"

    @property
    def has_channels_info(self) -> bool:
        """Returns True if channel count is known."""
        return self.channels is not None

    @property
    def has_sample_rate(self) -> bool:
        """Returns True if sample rate is known."""
        return self.sample_rate is not None

    @property
    def has_codec_info(self) -> bool:
        """Returns True if audio codec information is present."""
        return self.audio_codec is not None

    @property
    def has_bit_depth(self) -> bool:
        """Returns True if bit depth information is present."""
        return self.bit_depth is not None

    @property
    def has_transcript(self) -> bool:
        """Returns True if transcript text is available."""
        return self.transcript is not None

    @property
    def has_file_hash(self) -> bool:
        """Returns True if file hash is available."""
        return self.file_hash is not None

    
    @property
    def is_stereo(self) -> Optional[bool]:
        """Returns True if audio has 2 channels."""
        if self.channels is not None:
            return self.channels == 2
        return None

    @property
    def is_mono(self) -> Optional[bool]:
        """Returns True if audio has 1 channel."""
        if self.channels is not None:
            return self.channels == 1
        return None

    @property
    def sample_rate_khz(self) -> Optional[float]:
        """Returns sample rate in kHz."""
        if self.sample_rate:
            return self.sample_rate / 1000
        return None

