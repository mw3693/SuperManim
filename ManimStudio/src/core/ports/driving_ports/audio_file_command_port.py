from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from src.core.entities.audio_file import AudioFile
from src.core.entities.audio_clip import AudioClip


class AudioFileCommandPort(ABC):
    @abstractmethod
    def add_audio(self, file_path: Path) -> AudioFile:
        """Add an audio file to the current project. Returns audio file entity."""
        pass

    @abstractmethod
    def remove_audio(self, audio_file_id: int, audio_file_name: Optional[str] = None) -> bool:
        """Remove an audio file by id or name. Returns success status."""
        pass

    @abstractmethod
    def list_audio_files(self) -> List[AudioFile]:
        """List all audio files in the current project."""
        pass




    @abstractmethod
    def get_audio_file_info(self, audio_file_id: int ) -> AudioFile:
        """Get detailed info about an audio file."""
        pass
