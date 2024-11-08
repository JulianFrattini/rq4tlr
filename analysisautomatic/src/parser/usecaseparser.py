from abc import ABC, abstractmethod
from util.uc import UseCase   

class AbstractUseCaseParser(ABC):
    
    @abstractmethod
    def parse(self, ucid: str, uc_text: str) -> UseCase:
        pass