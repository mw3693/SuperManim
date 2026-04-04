# Location: src/core/ports/driving_ports/export_command_port.py

from abc import ABC, abstractmethod
from pathlib import Path
from src.core.constants import VideoFormat, RenderQuality

class ExportCommandPort(ABC):
    """
    Driving Port: Defines the interface for final video production and assembly.
    Implemented by the ExportService to handle multi-scene merging and encoding.
    """

    @abstractmethod
    def export_scene(
        self, 
        scene_id: int, 
        output_path: Path, 
        format: VideoFormat = VideoFormat.MP4, 
        quality: RenderQuality = RenderQuality.HIGH, 
        include_audio: bool = True
    ) -> Path:
        """
        Render and export a specific scene to a standalone file.
        
        Args:
            scene_id: Unique identifier of the target scene.
            output_path: Directory where the exported file will be saved.
            format: Target container format (mp4, mov, png).
            quality: Desired render quality preset.
            include_audio: Toggle to include/exclude audio tracks in the output.
            
        Returns:
            Path: The absolute path to the generated file.
        """
        pass

    @abstractmethod
    def export_project(
        self, 
        output_path: Path, 
        format: VideoFormat = VideoFormat.MP4, 
        quality: RenderQuality = RenderQuality.HIGH,
        include_audio: bool = True
    ) -> Path:
        """
        Concatenate all project scenes into a single final master video.
        
        Args:
            output_path: Destination directory for the full project export.
            format: Final video container format.
            quality: Global quality preset for the entire assembly.
            include_audio: Global toggle for audio inclusion.
            
        Returns:
            Path: The absolute path to the final project master file.
        """
        pass
