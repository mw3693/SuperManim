# core/entities/project_settings.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

# Using TYPE_CHECKING to avoid circular imports during type hinting
if TYPE_CHECKING:
    from .render_settings import RenderSettings
    from .audio_settings import AudioSettings
    from .video_settings import VideoSettings
    from .export_settings import ExportSettings


@dataclass(slots=True, kw_only=True)
class ProjectSettings:
    render_settings: Optional[RenderSettings] = None
    audio_settings:  Optional[AudioSettings]  = None
    video_settings:  Optional[VideoSettings]  = None
    export_settings: Optional[ExportSettings] = None
