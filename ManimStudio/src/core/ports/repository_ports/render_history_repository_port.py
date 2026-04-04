from abc import ABC, abstractmethod

class RenderHistoryRepositoryPort(ABC):
    @abstractmethod
    def save_render_job(self, scene_id, status, started_at=None, finished_at=None, error_message=None) -> int:
        pass

    @abstractmethod
    def list_render_jobs(self) -> list:
        pass

    @abstractmethod
    def get_latest_job_for_scene(self, scene_id) -> dict:
        pass
