# core/entities/project.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

# Using TYPE_CHECKING to avoid circular imports during type hinting
if TYPE_CHECKING:
    from .media_unit import MediaUnit
    from .render_settings import RenderSettings
    from .audio_settings import AudioSettings
    from .video_settings import VideoSettings
    from .export_settings import ExportSettings

@dataclass
class Project:
    """
    The Project Entity represents one complete video production workspace.
    It is a pure data container holding identifying info, location data, 
    settings, and the list of media items.
    """

    # -- IDENTITY --
    project_name: str

    # -- LOCATION --
    # Paths for project folders and database storage
    project_folder_path: Optional[str] = None
    project_db_path: Optional[str] = None

    # -- TIMESTAMPS --
    # ISO formatted strings for creation and last update
    project_created_at: Optional[str] = None
    project_updated_at: Optional[str] = None

    # -- CONTENT --
    # List of MediaUnit objects (audio clips, video clips, or Manim scenes)
    # Using field(default_factory=list) ensures a fresh list for every new project
    project_items: List[MediaUnit] = field(default_factory=list)

    # -- SETTINGS (Optional components) --
    project_render_settings: Optional[RenderSettings] = None
    project_audio_settings:  Optional[AudioSettings]  = None
    project_video_settings:  Optional[VideoSettings]  = None
    project_export_settings: Optional[ExportSettings] = None

    # -- STATE --
    # 1 = Open (Active in memory), 0 = Closed
    project_state: int = 0
