from abc import ABC, abstractmethod

from src.structure.subflow import SubFlow


class SubflowProcessor(ABC):

    @property
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def process(self, subflow: SubFlow):
        pass