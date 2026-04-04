from abc import ABC, abstractmethod

class AssetManagerPort(ABC):
    @abstractmethod
    def store_asset(self, source_path: str, asset_name: str, asset_type: str = "image") -> dict:
        pass

    @abstractmethod
    def list_assets(self) -> list:
        pass

    @abstractmethod
    def retrieve_asset(self, asset_name: str) -> str:
        pass

    @abstractmethod
    def delete_asset(self, asset_name: str) -> bool:
        pass
