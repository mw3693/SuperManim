from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Optional
from src.core.entities.timeline import Timeline
from src.core.entities.project_settings import ProjectSettings
from config.constants import (
             AUDIO_CLIPS_DIR,
             VIDEO_CLIPS_DIR,
             SCENES_DIR,
             PREVIEWS_DIR,
             EXPORTS_DIR,
             PROJECT_DB_FILENAME
        )

@dataclass (slots = True, kw_only=True)
class Project:
    root_path        : Path
    settings         : ProjectSettings
    timeline         : Timeline
     
    @property
    def name(self) -> str:
        return self.root_path.name


    @property
    def exports_path(self) -> Path:
        """Returns the path where the final rendered video will be saved."""
        return self.root_path / EXPORTS_DIR

    @property
    def preview_path(self) -> Path:
        """Returns the central directory for p."""
        return self.root_path / PREVIEWS_DIR

    @property
    def scenes_path(self) -> Path:
        """Returns the central directory for p."""
        return self.root_path / SCENES_DIR

    @property
    def video_clips_path(self) -> Path:
        return self.root_path / VIDEO_CLIPS_DIR

    @property
    def audio_clips_path(self) -> Path:
        return self.root_path / AUDIO_CLIPS_DIR



    @property
    def project_data_path(self) -> Path:
        return self.root_path / PROJECT_DB_FILENAME
