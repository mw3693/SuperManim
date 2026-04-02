from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

@dataclass
class Scene:
    """
    The Scene Entity represents a single, independent unit of animation.
    It acts as a data container for metadata, timing, and rendering state.
    
    All timing values are stored in MILLISECONDS (int) to avoid float errors.
    """

    # -- MANDATORY CONFIGURATION --
    scene_resolution: str  # e.g., "1920x1080"
    scene_fps: int         # e.g., 30, 60

    # -- GROUP 1: IDENTITY --
    scene_id: int = 0
    scene_index: int = 0
    scene_name: str = "unnamed_scene"
    previous_scene_id: Optional[int] = None
    next_scene_id: Optional[int] = None

    # -- GROUP 2: TIMING (In Milliseconds) --
    scene_duration: int = 0
    scene_start_time: int = 0
    scene_end_time: int = 0
    scene_start_marker: Optional[str] = None
    scene_end_marker: Optional[str] = None

    # -- GROUP 3: CODE & PATHS --
    # Using Path objects instead of strings for robust file handling
    scene_code_path: Optional[Path] = None
    scene_code_content: Optional[str] = None
    scene_output_path: Optional[Path] = None
    scene_preview_path: Optional[Path] = None

    # -- GROUP 4: HASH FINGERPRINTS (For Change Detection) --
    scene_code_hash: Optional[str] = None
    scene_assets_hash: Optional[str] = None
    scene_audio_hash: Optional[str] = None
    final_scene_hash: Optional[str] = None

    # -- GROUP 5: VISUALS & STATUS --
    scene_background_color: str = "#000000"
    scene_status: str = "pending"  # pending, rendered, failed, modified, skipped
    scene_error_message: Optional[str] = None
    scene_rendered_at: Optional[datetime] = None
    scene_render_duration: Optional[int] = None

    # -- GROUP 6: AUDIO LINKS --
    related_audio_clip_path: Optional[Path] = None
    synced_with_audio: bool = False

    def __post_init__(self):
        """
        Validation and Type Enforcement Guard.
        Ensures the scene state is physically possible and types are consistent.
        """
        # 1. Basic Validation
        if self.scene_fps <= 0:
            raise ValueError(f"Scene FPS must be positive, got {self.scene_fps}")
        
        if self.scene_duration < 0:
            raise ValueError("Scene duration cannot be negative.")

        # 2. Path Enforcement (Convert strings to Path objects automatically)
        path_fields = [
            'scene_code_path', 
            'scene_output_path', 
            'scene_preview_path', 
            'related_audio_clip_path'
        ]
        
        for field_name in path_fields:
            value = getattr(self, field_name)
            if isinstance(value, str):
                setattr(self, field_name, Path(value))

        # 3. String Sanitization
        if not self.scene_name.strip():
            self.scene_name = f"scene_{self.scene_index}"
