from abc import ABC, abstractmethod

class FileStoragePort(ABC):
    @abstractmethod
    def save_file(self, source_path: str, destination_path: str) -> str:
        pass

    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def read_file(self, file_path: str) -> bytes:
        pass

    @abstractmethod
    def ensure_directory(self, dir_path: str) -> None:
        pass

    @abstractmethod
    def delete_directory(self, dir_path: str) -> bool:
        pass

    @abstractmethod
    def copy_directory(self, src: str, dst: str) -> None:
        pass

    @abstractmethod
    def list_files(self, dir_path: str) -> list:
        pass
