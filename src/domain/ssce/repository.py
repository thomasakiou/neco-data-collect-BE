from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.ssce.entities import SSCE

class SSCERepository(ABC):
    @abstractmethod
    def get_by_id(self, ssce_id: int) -> Optional[SSCE]:
        pass

    @abstractmethod
    def save(self, ssce: SSCE) -> SSCE:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[SSCE]:
        pass

    @abstractmethod
    def delete(self, ssce_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, ssce_id: int, **kwargs) -> Optional[SSCE]:
        pass

    @abstractmethod
    def bulk_create(self, ssce_list: List[SSCE]) -> int:
        pass

    @abstractmethod
    def bulk_delete(self, ssce_ids: List[int]) -> int:
        pass
