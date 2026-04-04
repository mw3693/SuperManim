# src/core/ports/driving_ports/project_command_port.py

from abc import ABC, abstractmethod
from pathlib import Path
from src.core.entities.project import Project
from src.core.entities.project_settings import ProjectSettings

class ProjectCommandPort(ABC):
    """
    Inbound Port: Defines the interface for project-level operations.
    This port is used by the outside world (CLI/GUI) to send commands to the Core.
    """

    @abstractmethod
    def create_project(self, name: str, root_path: Path = None) -> Project:
        """
        Creates a new project structure and initializes its metadata.
        Returns the newly created Project entity.
        """
        pass

    @abstractmethod
    def open_project(self, path: Path) -> Project:
        """
        Opens an existing project from the specified directory path.
        Returns the loaded Project entity.
        """
        pass

    @abstractmethod
    def close_project(self) -> None:
        """
        Closes the currently active project and releases associated resources.
        """
        pass

    @abstractmethod
    def delete_project(self, path: Path) -> bool:
        """
        Deletes a project directory and its database entries.
        Returns True if the operation was successful.
        """
        pass

    @abstractmethod
    def update_project_settings(self, **kwargs) -> None:
        """
        Updates specific project settings fields using keyword arguments.
        Only the provided fields will be modified.
        """
        pass

    @abstractmethod
    def get_project_settings(self) -> ProjectSettings:
        """
        Retrieves the current ProjectSettings entity for the active project.
        """
        pass

    @abstractmethod
    def get_recent_projects(self) -> list:
        """
        Returns a list of recently opened project paths (Path objects) or summaries.
        """
        pass
