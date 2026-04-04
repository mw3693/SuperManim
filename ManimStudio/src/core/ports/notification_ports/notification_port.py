from abc import ABC, abstractmethod

class NotificationPort(ABC):
    @abstractmethod
    def success(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def info(self, message: str) -> None:
        pass
