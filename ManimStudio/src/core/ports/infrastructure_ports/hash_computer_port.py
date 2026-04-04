from abc import ABC, abstractmethod

class HashComputerPort(ABC):
    @abstractmethod
    def compute_hash(self, file_path: str) -> str:
        pass
