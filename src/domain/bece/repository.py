from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.bece.entities import BECE

class BECERepository(ABC):
    @abstractmethod
    def get_by_id(self, bece_id: int) -> Optional[BECE]:
        pass

    @abstractmethod
    def save(self, bece: BECE) -> BECE:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[BECE]:
        pass

    @abstractmethod
    def delete(self, bece_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, bece_id: int, **kwargs) -> Optional[BECE]:
        pass

    @abstractmethod
    def bulk_create(self, bece_list: List[BECE]) -> int:
        pass

    @abstractmethod
    def bulk_delete(self, bece_ids: List[int]) -> int:
        pass
