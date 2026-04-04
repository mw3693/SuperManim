from abc import ABC, abstractmethod

class SessionRepositoryPort(ABC):
    @abstractmethod
    def load_session(self) -> dict:
        pass

    @abstractmethod
    def save_session(self, is_project_open, last_project_name=None, last_project_path=None, last_opened_at=None) -> None:
        pass

    @abstractmethod
    def add_recent_project(self, project_name, project_path, last_opened_at) -> None:
        pass

    @abstractmethod
    def get_recent_projects(self) -> list:
        pass

    @abstractmethod
    def clear_recent_projects(self) -> None:
        pass
