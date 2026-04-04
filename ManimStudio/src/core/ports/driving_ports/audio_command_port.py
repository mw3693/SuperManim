from abc import ABC, abstractmethod

class AudioCommandPort(ABC):
    @abstractmethod
    def add_audio(self, file_path: str) -> dict:
        """Add an audio file to the current project. Returns audio file dict."""
        pass

    @abstractmethod
    def remove_audio(self, audio_id: int = None, file_name: str = None) -> bool:
        """Remove an audio file by id or name. Returns success status."""
        pass

    @abstractmethod
    def list_audio_files(self) -> list:
        """List all audio files in the current project."""
        pass

    @abstractmethod
    def set_active_audio(self, audio_id: int) -> None:
        """Set the active audio file for the project."""
        pass

    @abstractmethod
    def get_active_audio(self) -> dict:
        """Get the currently active audio file. Returns dict or None."""
        pass

    @abstractmethod
    def auto_split_audio(self, threshold_db: float = -40, min_silence_sec: float = 0.5) -> list:
        """Auto-split active audio by silence detection. Returns list of audio clip dicts."""
        pass

    @abstractmethod
    def list_audio_clips(self) -> list:
        """List all audio clips for the active audio."""
        pass

    @abstractmethod
    def get_clip_for_scene(self, scene_id: int) -> dict:
        """Get the audio clip assigned to a scene. Returns clip dict or None."""
        pass

    @abstractmethod
    def get_audio_info(self, audio_id: int = None) -> dict:
        """Get detailed info about an audio file."""
        pass
