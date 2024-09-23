from abc import ABCMeta, abstractmethod

from domain.model import KakakuItem


class IPreviousDaysKakakuData(metaclass=ABCMeta):
    @abstractmethod
    async def get(self) -> list[KakakuItem]:
        pass
