from abc import ABC, abstractmethod

class ProjectRepositoryPort(ABC):
    @abstractmethod
    def save_project(self, name: str, path: str, mode: str = "manim") -> int:
        """Create a new project record. Returns project id."""
        pass

    @abstractmethod
    def list_projects(self) -> list:
        """Return all projects as list of dicts with keys: name, path, created_at."""
        pass

    @abstractmethod
    def delete_project(self, project_path: str) -> bool:
        """Delete a project record by path."""
        pass

    @abstractmethod
    def project_exists(self, project_name: str) -> bool:
        """Check if a project with given name exists."""
        pass
