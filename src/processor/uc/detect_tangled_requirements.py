from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class DetectTangledRequirements(UCProcessor):

    name: str = "tangled_requirements"

    def process(self, uc: UseCase) -> bool:
        """
        Detects when a use case contains descriptions of several requirements or different functionalities i.e., has trace links to multiple target artifacts
        
        :param uc: the use case to process

        :return: True if the use case conveys tangled requirements, False otherwise
        """
        return len(uc.goldstandard.links[uc.id]) > 1
