from processor.absprocessor import AbsProcessor
from util.uc import UseCase

class CalculateLargeUseCases(AbsProcessor):

    name: str = "large_ucs"

    def process(self, uc: UseCase) -> bool:
        """
        Calculates the size of a use case as the total number of steps and alternative steps
        """
        return len(uc.steps) + len(uc.alternative)