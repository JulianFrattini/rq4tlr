from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class CalculateSimilarity(UCProcessor):

    name: str = "similarity"
    threshold: float = 0.994

    def process(self, uc: UseCase) -> bool:
        """
        Checks whteher this use case is highly similar to any other use case
        
        :param uc: the use case to process

        :return: True if the use case is highly similar to another use case, False otherwise
        """
        return any(value > self.threshold for value in uc.similarities.values())
