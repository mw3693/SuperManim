from abc import ABC, abstractmethod

class AudioRepositoryPort(ABC):
    @abstractmethod
    def add_audio_file(self, stored_path: str, audio_format: str, duration: float, **kwargs) -> int:
        pass

    @abstractmethod
    def get_active_audio(self) -> dict:
        pass

    @abstractmethod
    def list_audio_files(self) -> list:
        pass

    @abstractmethod
    def set_active_audio(self, audio_id: int) -> None:
        pass

    @abstractmethod
    def delete_audio(self, audio_id: int) -> bool:
        pass

    @abstractmethod
    def add_audio_clip(self, scene_id, clip_path, clip_duration, start_in_original, end_in_original) -> int:
        pass

    @abstractmethod
    def list_audio_clips(self) -> list:
        pass

    @abstractmethod
    def get_clip_for_scene(self, scene_id: int) -> dict:
        pass
