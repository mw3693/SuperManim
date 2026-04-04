from abc import ABC, abstractmethod
from pathlib import Path 
from src.core.entities.scene import Scene
from src.core.entities.scene_code import SceneCode

from src.core.entities.scene_audio import SceneAudio



class SceneCommandPort(ABC):
    @abstractmethod
    def add_scene(self, scene_name: str, code: SceneCode = None, duration: int = None) -> Scene:
        """Add a new scene to the current project. Returns scene Entity."""
        pass

    @abstractmethod
    def remove_scene(self, scene_id: int ) -> bool:
        """Remove a scene by id . Returns success status."""
        pass

    @abstractmethod
    def list_scenes(self) -> list:
        """List all scenes in the current project. Returns list of scene entities."""
        pass

    @abstractmethod
    def update_scene(self, scene_id: int, **kwargs) -> Scene:
        """Update a scene's properties. Returns updated scene Entity."""
        pass

    @abstractmethod
    def reorder_scenes(self, scene_ids: list) -> None:
        """Reorder scenes to match the given list of scene_ids."""
        pass

    @abstractmethod
    def get_scene(self, scene_id: int) -> Scene:
        """Get a scene by id . Returns scene entity or None."""
        pass

    @abstractmethod
    def edit_scene_code(self, scene_id: int, code: SceneCode) -> Scene:
        """Update the code for a scene. Returns updated scene entity."""
        pass
