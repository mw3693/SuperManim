from abc import ABC, abstractmethod

class CacheRepositoryPort(ABC):
    @abstractmethod
    def save_hash(self, scene_id: int, code_hash: str, video_path: str = None) -> None:
        pass

    @abstractmethod
    def load_hash(self, scene_id: int) -> dict:
        """Returns dict with code_hash, is_valid, video_path or None."""
        pass

    @abstractmethod
    def invalidate_hash(self, scene_id: int) -> None:
        pass

    @abstractmethod
    def get_all_cache_records(self) -> list:
        pass
