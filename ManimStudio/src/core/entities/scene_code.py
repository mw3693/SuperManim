from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import hashlib
import datetime


@dataclass(slots=True, kw_only=True)
class SceneCode:
    """
    Represents a Python code file for a Manim scene.
    This is a rich entity with full metadata and useful properties.
    No business logic (like file I/O) is included.
    """

    scene_code_id: int                  # Unique ID for this SceneCode entity
    scene_id: int                       # The ID of the parent Scene
    scene_code_path: Path               # Path to the Python file
    scene_code_content: Optional[str] = None  # Optional content if already loaded

    # Optional metadata
    file_hash: Optional[str] = None     # Hash of the content for caching or comparison
   
    @property
    def has_content(self) -> bool:
        """Returns True if the code content is loaded in memory."""
        return self.scene_code_content is not None

    @property
    def is_hashed(self) -> bool:
        """Returns True if the content has a hash calculated."""
        return self.file_hash is not None

    
    @property
    def filename(self) -> str:
        """Returns the file name from the path."""
        return self.scene_code_path.name

   
