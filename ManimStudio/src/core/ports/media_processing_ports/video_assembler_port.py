from abc import ABC, abstractmethod

class VideoAssemblerPort(ABC):
    @abstractmethod
    def assemble_clips(self, clip_paths: list, output_path: str) -> str:
        """Join multiple video clips. Returns output path."""
        pass

    @abstractmethod
    def merge_audio_video(self, video_path: str, audio_path: str, output_path: str) -> str:
        pass

    @abstractmethod
    def remove_audio_from_video(self, video_path: str, output_path: str) -> str:
        pass

    @abstractmethod
    def trim_video(self, input_path: str, start_sec: float, end_sec: float, output_path: str) -> str:
        pass
