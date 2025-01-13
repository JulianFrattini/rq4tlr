from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class DetectHappyUCs(UCProcessor):

    name: str = "happy_ucs"

    def process(self, uc: UseCase) -> bool:
        """
        Detects if a use case is happy or not, i.e., whether it contains alternative steps or not
        
        :param uc: the use case to process

        :return: True if the use case is happy, False otherwise
        """
        return len(uc.alternative) == 0