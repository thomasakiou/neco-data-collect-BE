from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.lga.entities import LGA

class LGARepository(ABC):
    @abstractmethod
    def get_by_id(self, lga_id: int) -> Optional[LGA]:
        pass

    @abstractmethod
    def save(self, lga: LGA) -> LGA:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[LGA]:
        pass

    @abstractmethod
    def delete(self, lga_id: int) -> bool:
        pass

    @abstractmethod
    def update(self, lga_id: int, **kwargs) -> Optional[LGA]:
        pass

    @abstractmethod
    def bulk_create(self, lga_list: List[LGA]) -> int:
        pass

    @abstractmethod
    def bulk_delete(self, lga_ids: List[int]) -> int:
        pass
