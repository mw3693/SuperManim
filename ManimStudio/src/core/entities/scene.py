from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from src.core.entities.scene_audio import SceneAudio
from src.core.entities.asset_file import AssetFile
from src.core.entities.scene_code import SceneCode


@dataclass(slots=True, kw_only=True)
class Scene:
    """
    Represents a Manim Scene with assets, audio, code, and metadata.
    Rich entity class with all key properties and safe defaults.
    """

    scene_id: int
    scene_root_path: Path                         # Path to scene folder, e.g., ProjectName/scenes/scene_01
    scene_index: Optional[int] = None
    scene_duration_ms: Optional[int] = None
    start_time_ms: Optional[int] = 0

    assets: List[AssetFile] = field(default_factory=list)
    related_audio: Optional[SceneAudio] = None
    related_code: Optional[SceneCode] = None
    scene_content: Optional[str] = None
    scene_hash: Optional[str] = None

    @property
    def scene_name(self) -> str:
        """Return a formatted scene name, e.g., 'scene_01'."""
        return f"scene_{self.scene_id:02d}"

    @property
    def end_time_ms(self) -> Optional[int]:
        """
        Compute end time in ms.
        Returns None if start time or duration is not defined.
        """
        if self.start_time_ms is None or self.scene_duration_ms is None:
            return None
        return self.start_time_ms + self.scene_duration_ms

    @property
    def has_assets(self) -> bool:
        return len(self.assets) > 0

    @property
    def has_audio(self) -> bool:
        return self.related_audio is not None

    @property
    def has_code(self) -> bool:
        return self.related_code is not None

    @property
    def has_content(self) -> bool:
        return self.scene_content is not None
