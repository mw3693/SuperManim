from abc import ABC, abstractmethod

class SceneCommandPort(ABC):
    @abstractmethod
    def add_scene(self, scene_name: str, code: str = None, duration: float = None) -> dict:
        """Add a new scene to the current project. Returns scene details dict."""
        pass

    @abstractmethod
    def remove_scene(self, scene_id: int = None, scene_index: int = None) -> bool:
        """Remove a scene by id or index. Returns success status."""
        pass

    @abstractmethod
    def list_scenes(self) -> list:
        """List all scenes in the current project. Returns list of scene dicts."""
        pass

    @abstractmethod
    def update_scene(self, scene_id: int, **kwargs) -> dict:
        """Update a scene's properties. Returns updated scene dict."""
        pass

    @abstractmethod
    def reorder_scenes(self, scene_ids: list) -> None:
        """Reorder scenes to match the given list of scene_ids."""
        pass

    @abstractmethod
    def get_scene(self, scene_id: int = None, scene_index: int = None) -> dict:
        """Get a scene by id or index. Returns scene dict or None."""
        pass

    @abstractmethod
    def edit_scene_code(self, scene_id: int, code: str) -> dict:
        """Update the code for a scene. Returns updated scene dict."""
        pass
