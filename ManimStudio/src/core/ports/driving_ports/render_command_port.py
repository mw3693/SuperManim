# Location: src/core/ports/driving_ports/render_command_port.py

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from src.core.constants import RenderQuality, DEFAULT_FPS, RenderStatus



class RenderCommandPort(ABC):
    """
    Driving Port: Defines the interface for internal scene rendering.
    Unlike Export, this is typically used for generating previews or 
    intermediate files during the editing process.
    """

    @abstractmethod
    def render_scene(
        self, 
        scene_id: int, 
        quality: RenderQuality = RenderQuality.HIGH, 
        fps: int = DEFAULT_FPS
    ) -> Path:
        """
        Triggers the render engine for a specific scene.
        
        Args:
            scene_id: The unique identifier of the scene to be rendered.
            quality: Render quality preset (from RenderQuality Enum).
            fps: Frames per second (defaults to system DEFAULT_FPS).
            
        Returns:
            Path: The absolute path to the rendered file.
        """
        pass

    @abstractmethod
    def render_all_scenes(
        self, 
        quality: RenderQuality = RenderQuality.HIGH, 
        fps: int = DEFAULT_FPS
    ) -> List[Path]:
        """
        Iterates through all scenes in the project and renders them sequentially.
        
        Args:
            quality: The quality preset to apply to all scenes.
            fps: The global FPS setting for this batch render.
            
        Returns:
            List[Path]: A list of file paths for all successfully rendered scenes.
        """
        pass

    @abstractmethod
    def get_render_status(self, scene_id: int) -> str:
        """
        Retrieves the current state of a render task (e.g., 'pending', 'rendered', 'skipped', 'failed').
        
        Args:
            scene_id: The identifier for the scene in question.
            
        Returns:
            str: A string representing the status.
        """
        pass

    @abstractmethod
    def get_project_render_status(self) -> List[SceneStatusInfo]:
        pass
    

    @abstractmethod
    def render_preview(self, scene_number: int, duration: float = 5.0) -> str:
        """Render a quick preview of a scene. Returns preview file path."""
        pass
