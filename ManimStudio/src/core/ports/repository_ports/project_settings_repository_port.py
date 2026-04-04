from abc import ABC, abstractmethod

class ProjectSettingsRepositoryPort(ABC):
    @abstractmethod
    def save_settings(self, project_name, project_path, created_at, **kwargs) -> None:
        pass

    @abstractmethod
    def load_settings(self) -> dict:
        """Returns dict of all settings."""
        pass

    @abstractmethod
    def update_settings(self, **kwargs) -> None:
        pass
