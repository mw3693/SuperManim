# core/entities/export_settings.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from constants import DEFAULT_VIDEO_FORMAT


@dataclass(slots=True, kw_only=True)
class ExportSettings:
    """
    ExportSettings stores all configuration for the final video
    assembly step — where rendered scene clips are stitched together
    into one complete output file.

    It describes the output format, quality level, filename, folder,
    codec, audio inclusion, export readiness, and optional watermark.

    This entity does not assemble video, invoke FFmpeg, or encode
    anything. It is a pure data container — a set of instructions
    that the export service reads to know how to package the final
    video.

    The project_is_export_ready flag is automatically maintained by
    the scene management service. It is True only when all scenes
    are rendered with zero pending and zero failed.
    """

    # === Output Format ===
    export_format: str = DEFAULT_VIDEO_FORMAT

    # === Output Quality ===
    export_quality: str = "high"

    # === Output Naming ===
    export_name: Optional[str] = None

    # === Audio ===
    export_include_audio: bool = True

    # === Codec ===
    export_codec: str = "libx264"
