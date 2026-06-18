from processor.subflow.subflowprocessor import SubflowProcessor

from structure.subflow import SubFlow


class CalculateMaxNumberOfReferencesToTargetArtifact(SubflowProcessor):

    name: str = "max_number_of_refs_to_target_artifacts"

    def process(self, subflow: SubFlow) -> int:
        """
        Counts the maximum number of links to any of the target artifacts associated with this subflow

        :param subflow: the subflow to process

        :return: the maximum number of links to any of the target artifacts associated with this subflow

        """
        targets = subflow.parent_uc.goldstandard.links[subflow.flow_id]
        maximum: int = 0
        for target in targets:
            # Get all entries where the target is in the list
            filtered_entries = {key: value for key, value in subflow.parent_uc.goldstandard.links.items() if target in value}
            if len(filtered_entries) > maximum:
                maximum = len(filtered_entries)
        return maximum
