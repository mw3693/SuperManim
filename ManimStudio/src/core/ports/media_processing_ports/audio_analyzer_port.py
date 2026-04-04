from abc import ABC, abstractmethod

class AudioAnalyzerPort(ABC):
    @abstractmethod
    def detect_silences(self, file_path: str, threshold_db: float = -40, min_silence_sec: float = 0.5) -> list:
        """Returns list of (start_sec, end_sec) silence intervals."""
        pass

    @abstractmethod
    def get_audio_info(self, file_path: str) -> dict:
        """Returns dict with duration, sample_rate, channels, format."""
        pass
