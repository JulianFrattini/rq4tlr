from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class CalculateLargeUseCases(UCProcessor):

    name: str = "large_ucs"

    def process(self, uc: UseCase) -> bool:
        """
        Calculates the size of a use case as the total number of steps and alternative steps
        """
        total_steps: int = 0
        for type in ['main', 'alternative']:
            subflows: dict[str, list] = getattr(uc, type)
            for subflow in subflows:
                total_steps += len(subflows[subflow])
        return total_steps