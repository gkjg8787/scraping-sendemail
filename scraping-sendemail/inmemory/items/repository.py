from domain.model import (
    KakakuItem,
    IKakakuItemRepository,
)


class KakakuItemDictRepository(IKakakuItemRepository):
    data: dict[int, KakakuItem]

    def __init__(self, data: dict[int, KakakuItem]):
        self.data = data

    async def save(self, kakakuitem: KakakuItem):
        self.data[kakakuitem.item_id] = kakakuitem

    async def find_by_item_id(self, item_id: int) -> KakakuItem | None:
        return self.data.get(item_id, None)

    async def find_all(self) -> list[KakakuItem]:
        return list(self.data.values())

    async def delete_by_item_id(self, item_id: int) -> None:
        if item_id in self.data:
            self.data.pop(item_id)
