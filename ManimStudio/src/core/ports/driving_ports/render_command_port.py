from abc import ABC, abstractmethod

class RenderCommandPort(ABC):
    @abstractmethod
    def render_scene(self, scene_number: int, quality: str = "high", fps: int = None) -> dict:
        """Render a single scene by its number (1-based index). Returns render result dict."""
        pass

    @abstractmethod
    def render_all_scenes(self, quality: str = "high", fps: int = None) -> list:
        """Render all scenes in order. Returns list of render result dicts."""
        pass

    @abstractmethod
    def render_preview(self, scene_number: int, duration: float = 5.0) -> str:
        """Render a quick preview of a scene. Returns preview file path."""
        pass

    @abstractmethod
    def get_render_status(self, scene_number: int) -> dict:
        """Get the latest render status for a scene."""
        pass

    @abstractmethod
    def get_render_history(self) -> list:
        """Get render history for all scenes."""
        pass

    @abstractmethod
    def cancel_render(self) -> bool:
        """Cancel the currently running render if any. Returns success status."""
        pass
