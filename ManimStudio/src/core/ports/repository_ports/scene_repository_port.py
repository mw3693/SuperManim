from abc import ABC, abstractmethod

class SceneRepositoryPort(ABC):
    @abstractmethod
    def create_scene(self, scene_name: str, scene_index: int, **kwargs) -> int:
        """Create a new scene. Returns scene_id."""
        pass

    @abstractmethod
    def get_scene(self, scene_id: int) -> dict:
        """Get a scene by id. Returns dict or None."""
        pass

    @abstractmethod
    def get_scene_by_index(self, scene_index: int) -> dict:
        pass

    @abstractmethod
    def list_scenes(self) -> list:
        """Return all scenes ordered by index."""
        pass

    @abstractmethod
    def update_scene(self, scene_id: int, **kwargs) -> None:
        pass

    @abstractmethod
    def delete_scene(self, scene_id: int) -> bool:
        pass

    @abstractmethod
    def get_scene_count(self) -> int:
        pass

    @abstractmethod
    def reorder_scenes(self, new_order: list) -> None:
        """new_order is list of scene_ids in desired order."""
        pass
