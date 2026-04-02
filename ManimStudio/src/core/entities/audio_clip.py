
# Location: SuperManim/src/core/entities/audio_clip.py
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict
from src.core.entities.media_unit import MediaUnit

@dataclass(slots=True, kw_only=True)
class AudioClip(MediaUnit):
  
    sample_rate : Optional[int] = None
    channels    : Optional[int] = None
    audio_codec : Optional[str] = None
    bit_depth   : Optional[int] = None


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

