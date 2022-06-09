from abc import abstractmethod
from typing import List

from models.device_schema import Device


class DatabaseManager:
    """
    This class is meant to be extended from
    ./mongo_manager.py which will be the actual connection to mongodb.
    """

    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    @abstractmethod
    async def connect_to_database(self, path: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def device_get_total(self) -> int:
        pass

    @abstractmethod
    async def device_get_actives(self) -> int:
        pass

    @abstractmethod
    async def device_get_all(self) -> List[Device]:
        pass

    @abstractmethod
    async def device_get_one(self, device_id: str) -> List[Device]:
        pass

    @abstractmethod
    async def device_insert_one(self, device: Device) -> List[Device]:
        pass

    @abstractmethod
    async def device_update_one(self, device: Device) -> List[Device]:
        pass

    @abstractmethod
    async def device_delete_one(self, device_id: str) -> List[Device]:
        pass

