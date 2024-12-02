from abc import ABC, abstractmethod
from util.uc import UseCase   

class AbsProcessor(ABC):

    @property
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def process(self, uc: UseCase):
        pass