from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class DetectMeaninglessUC(UCProcessor):

    name: str = "meaningless_uc"

    def process(self, uc: UseCase) -> bool:
        """
        Detects if a use case is a wrongly defined or meaningless use case that does not contribute to the requirements specification i.e., has no trace links in the goldstandard
        
        :param uc: the use case to process

        :return: True if the use case is meaningless, False otherwise
        """
        return not uc.id in uc.goldstandard.links
