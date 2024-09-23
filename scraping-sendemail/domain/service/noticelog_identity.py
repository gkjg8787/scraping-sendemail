from abc import ABCMeta, abstractmethod


class INoticeLogIdentity(metaclass=ABCMeta):
    @abstractmethod
    async def next_identity(self) -> str:
        pass
