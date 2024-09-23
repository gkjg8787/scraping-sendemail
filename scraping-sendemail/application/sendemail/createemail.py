from abc import ABCMeta, abstractmethod


class Async_MessageCreator(metaclass=ABCMeta):
    @abstractmethod
    async def get_message(self) -> str:
        pass


class OneMailCreator:
    async_msgcreators: list[Async_MessageCreator]

    def __init__(
        self,
        async_msgcreators: list[Async_MessageCreator] = [],
    ):
        self.async_msgcreators = async_msgcreators

    def add_async_messagecreator(self, async_msgcreator: Async_MessageCreator):
        if not self.async_msgcreators:
            self.async_msgcreators = [async_msgcreator]
        else:
            self.async_msgcreators.add(async_msgcreator)

    async def execute(self) -> str:
        message: str = ""
        for a in self.async_msgcreators:
            result = await a.get_message()
            if result:
                message += result
        return message
