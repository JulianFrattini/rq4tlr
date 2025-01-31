from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class DetectScatteredRequirements(UCProcessor):

    name: str = "scattered_requirements"

    def process(self, uc: UseCase) -> bool:
        """
        Detects when the specification of one functionality is not encapsulated in a single use case i.e., a target artifact is linking to this use case and others as well
        
        :param uc: the use case to process

        :return: True if the use case is part of scattered requirements, False otherwise
        """
        for flow in uc.main | uc.alternative:
            if flow in uc.goldstandard.links:
                targets = uc.goldstandard.links[flow]
                for target in targets:
                    # Get all entries where the target is in the list
                    filtered_entries = {key: value for key, value in uc.goldstandard.links.items() if target in value}
                    if len(filtered_entries) > 1:
                        return True
        return False
