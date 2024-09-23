from abc import ABCMeta, abstractmethod

from .items import KakakuItem


class IKakakuItemRepository(metaclass=ABCMeta):
    @abstractmethod
    async def save(self, newestitem: KakakuItem):
        pass

    @abstractmethod
    async def find_by_item_id(self, item_id: int) -> KakakuItem | None:
        pass

    @abstractmethod
    async def find_all(self) -> list[KakakuItem]:
        pass

    @abstractmethod
    async def delete_by_item_id(self, item_id: int) -> None:
        pass
