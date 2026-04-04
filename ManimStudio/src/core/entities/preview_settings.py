# core/entities/preview_settings.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from constants import (
    DEFAULT_VIDEO_FORMAT,
    DEFAULT_VIDEO_CODEC,
    PREVIEW_VIDEO_WIDTH,
    PREVIEW_VIDEO_HEIGHT,
    PREVIEW_FPS,
    PREVIEW_CRF,
)

@dataclass(slots=True, kw_only=True)
class PreviewSettings:
    """
    PreviewSettings stores configuration for low-quality preview renders.
    Previews are fast, lightweight renders meant for checking timing,
    layout, and composition before committing to a full-quality export.
    This entity does not perform rendering or invoke FFmpeg.
    It is a pure data container read by the preview service.
    """

    # === Resolution ===
    # Downscaled resolution for fast rendering (default: 854x480 / 480p)
    preview_width:  int = PREVIEW_VIDEO_WIDTH
    preview_height: int = PREVIEW_VIDEO_HEIGHT

    # === Frame Rate ===
    # Lower FPS speeds up the preview render significantly
    preview_fps: int = PREVIEW_FPS

    # === Quality ===
    # CRF value for libx264 — higher = smaller file / lower quality
    # Range: 0 (lossless) → 51 (worst). 35 is a good preview trade-off.
    preview_crf: int = PREVIEW_CRF

    # === Format & Codec ===
    preview_format: str = DEFAULT_VIDEO_FORMAT
    preview_codec:  str = DEFAULT_VIDEO_CODEC

    # === Audio ===
    # Skip audio during preview to reduce render time
    preview_include_audio: bool = False

    # === Output ===
    # Custom output name for the preview file; defaults to project name
    preview_name: Optional[str] = None
