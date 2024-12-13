from abc import ABC, abstractmethod
from util.uc import RawUseCase 

class AbstractUseCaseParser(ABC):
    
    @abstractmethod
    def parse(self, ucid: str, uc_text: str) -> RawUseCase:
        """Parse a raw use case text into a RawUseCase object.
        
        Args:
            ucid (str): The unique identifier of the use case.
            uc_text (str): The raw use case text.
            
        Returns: a raw use case object."""
        pass