from abc import ABC, abstractmethod

class ProgressReporterPort(ABC):
    @abstractmethod
    def start_progress(self, total: int, description: str = "") -> None:
        pass

    @abstractmethod
    def update_progress(self, current: int, description: str = "") -> None:
        pass

    @abstractmethod
    def finish_progress(self, message: str = "Done.") -> None:
        pass
