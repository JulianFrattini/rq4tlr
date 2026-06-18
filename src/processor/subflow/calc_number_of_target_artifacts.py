from processor.subflow.subflowprocessor import SubflowProcessor

from structure.subflow import SubFlow


class CalculateNumberOfTargetArtifacts(SubflowProcessor):

    name: str = "number_of_linked_target_artifacts"

    def process(self, subflow: SubFlow) -> int:
        """
        Counts the number of target artifacts associated with this subflow

        :param subflow: the subflow to process

        :return: the number of target artifacts associated with this subflow

        """
        return len(subflow.parent_uc.goldstandard.links[subflow.flow_id])
