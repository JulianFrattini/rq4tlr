from abc import ABC, abstractmethod
from structure.rawusecase import RawUseCase

class AbstractUseCaseParser(ABC):
    
    @abstractmethod
    def parse(self, ucid: str, uc_texts: dict[str, str], uc_name: str=None) -> RawUseCase:
        """Parse a raw use case text into a RawUseCase object.
        
        Args:
            ucid (str): The unique identifier of the use case.
            uc_texts (dict[str, str]): The raw use case texts.
            
        Returns: a raw use case object."""
        pass