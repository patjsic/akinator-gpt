from abc import ABC, abstractmethod

class Model(ABC):
    """Abstract class for models to be used in `aki.py`. File assumes having these two methods, but for now attributes can be flexible.
    """
    @abstractmethod
    def answer(self, question:str) -> str:
        pass

    @abstractmethod
    def history(self) -> str:
        pass

