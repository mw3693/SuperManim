from abc import ABC, abstractmethod

class PreviewGeneratorPort(ABC):
    @abstractmethod
    def generate_preview(self, scene_file: str, output_path: str, duration: float, fps: int = 15) -> str:
        pass
