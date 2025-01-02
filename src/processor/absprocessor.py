from abc import ABC, abstractmethod
from structure.usecase import UseCase   

class AbsProcessor(ABC):

    @property
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def process(self, uc: UseCase):
        pass