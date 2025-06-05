from abc import ABC, abstractmethod

class InsercionBase(ABC):
    @abstractmethod
    def ejecutar(self, session):
        pass
