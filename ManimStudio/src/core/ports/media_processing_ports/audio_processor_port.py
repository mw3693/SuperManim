from abc import ABC, abstractmethod

class AudioProcessorPort(ABC):
    @abstractmethod
    def get_audio_duration(self, file_path: str) -> float:
        """Returns duration in seconds."""
        pass

    @abstractmethod
    def split_audio(self, input_path: str, start_sec: float, end_sec: float, output_path: str) -> str:
        """Split audio file. Returns output path."""
        pass

    @abstractmethod
    def convert_audio(self, input_path: str, output_format: str, output_path: str) -> str:
        """Convert audio format. Returns output path."""
        pass

    @abstractmethod
    def trim_audio(self, input_path: str, start_sec: float, end_sec: float, output_path: str) -> str:
        pass

    @abstractmethod
    def merge_audio(self, file_path1: str, file_path2: str, output_path: str) -> str:
        pass

    @abstractmethod
    def extract_audio_from_video(self, video_path: str, output_path: str) -> str:
        pass
