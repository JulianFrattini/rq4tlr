from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class DetectNonFunctionalRequirements(UCProcessor):

    name: str = "nfrs"

    def process(self, uc: UseCase) -> bool:
        """
        Detects whether a use cases contains any items in the quality_requirements section
        """
        return len(uc.quality_requirements) > 0
