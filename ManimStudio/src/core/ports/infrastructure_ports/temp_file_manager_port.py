from abc import ABC, abstractmethod

class TempFileManagerPort(ABC):
    @abstractmethod
    def create_temp_file(self, suffix: str = ".tmp") -> str:
        pass

    @abstractmethod
    def create_temp_directory(self) -> str:
        pass

    @abstractmethod
    def cleanup_temp_files(self, base_dir: str = None) -> int:
        pass
