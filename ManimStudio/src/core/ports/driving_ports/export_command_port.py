from abc import ABC, abstractmethod

class ExportCommandPort(ABC):
    @abstractmethod
    def export_scene(self, scene_number: int, output_path: str, format: str = "mp4", include_audio: bool = True) -> str:
        """Export a single scene to file. Returns output file path."""
        pass

    @abstractmethod
    def export_project(self, output_path: str, format: str = "mp4", include_audio: bool = True) -> str:
        """Export the entire project (all scenes assembled) to file. Returns output file path."""
        pass

    @abstractmethod
    def export_with_custom_audio(self, scene_number: int, audio_path: str, output_path: str) -> str:
        """Export a scene merged with a custom audio file. Returns output file path."""
        pass
