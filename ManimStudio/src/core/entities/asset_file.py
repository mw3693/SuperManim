# Location: SuperManim/src/core/entities/asset_file.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from enum import Enum


class AssetType(Enum):
    """Enum representing the type of an asset."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"


@dataclass(slots=True, kw_only=True)
class AssetFile:
    """
    Represents a physical asset file used in a scene.
    
    Attributes:
        id: Unique identifier for the asset.
        file_path: Path to the asset file on disk.
        type: Type of the asset (IMAGE, VIDEO, AUDIO, OTHER).
        size_bytes: File size in bytes.
        mime_type: Optional MIME type of the file (e.g., "image/png").
        file_hash: Optional hash of the file for integrity checking.
    """
    id: int
    file_path: Path
    type: AssetType
    size_bytes: int
    mime_type: Optional[str] = None
    file_hash: Optional[str] = None

    def __post_init__(self) -> None:
        """Post-initialization validation for critical fields."""
        # Ensure file_path is a Path instance
        if not isinstance(self.file_path, Path):
            raise TypeError("file_path must be a pathlib.Path instance")
        # Ensure size is non-negative
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be >= 0")

    @property
    def extension(self) -> str:
        """
        Returns the file extension (including the dot), in lowercase.
        
        Example:
            Path("video.mp4") -> ".mp4"
        """
        return self.file_path.suffix[1:].lower()

    @property
    def filename(self) -> str:
        """
        Returns the name of the file including extension.
        
        Example:
            Path("/path/to/audio.wav") -> "audio.wav"
        """
        return self.file_path.name

    def is_image(self) -> bool:
        """Returns True if the asset type is IMAGE."""
        return self.type == AssetType.IMAGE

    def is_video(self) -> bool:
        """Returns True if the asset type is VIDEO."""
        return self.type == AssetType.VIDEO

    def is_audio(self) -> bool:
        """Returns True if the asset type is AUDIO."""
        return self.type == AssetType.AUDIO
