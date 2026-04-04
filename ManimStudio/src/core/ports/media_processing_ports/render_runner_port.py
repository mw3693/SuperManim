from abc import ABC, abstractmethod

class RenderResult:
    def __init__(self, succeeded: bool, output_path: str = None, elapsed_time: float = 0.0, error: str = None):
        self.succeeded = succeeded
        self.output_path = output_path
        self.elapsed_time = elapsed_time
        self.error = error

class RenderRunnerPort(ABC):
    @abstractmethod
    def render_scene(self, scene_file: str, output_path: str, duration: float, fps: int = 30, quality: str = "high") -> RenderResult:
        pass
