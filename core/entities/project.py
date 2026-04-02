from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Import other entities for type hinting only
from .scenes import Scene
from .project_settings import ProjectSettings

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
    project_folder_path: Path 
    project_db_path: Path

    # -- COMPOSITION --
    # A list to hold Scene entities associated with this project
    project_scenes_list: List['Scene'] = field(default_factory=list)

    # -- SETTINGS --
    project_settings: Optional[ProjectSettings] = None

    # -- TIMESTAMPS --
    # Captures the exact moment the project object is initialized
    project_created_at: Optional[str] = None
    
    # -- STATE --
    # Tracks if the project is currently active/open in the application
    project_state: bool = False

    def __post_init__(self):
        """
        Internal validation logic executed immediately after the object is created.
        This ensures the entity always maintains a valid state.
        """
        # 1. Validation: Ensure the project name is not empty or just whitespace
        if not self.project_name or not self.project_name.strip():
            raise ValueError("Project name cannot be empty.")

        # 2. Type Enforcement: Automatically convert string paths to Path objects 
        # to ensure consistency across the entire application.
        if isinstance(self.project_folder_path, str):
            self.project_folder_path = Path(self.project_folder_path)
            
        if isinstance(self.project_db_path, str):
            self.project_db_path = Path(self.project_db_path)
