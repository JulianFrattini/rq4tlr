from processor.subflow.subflowprocessor import SubflowProcessor

from structure.sentence import sentence

from structure.subflow import SubFlow


class CalculateCoherence(SubflowProcessor):

    name: str = "coherence"

    def process(self, subflow: SubFlow) -> float:
        """
        Calculates the coherence of a use case. The coherence is defined as the number of steps with a predecessor where the step repeats at least one noun from the predecessor divided by the total number of steps with a predecessor.
        """
        steps_with_predecessor: float = 0
        steps_with_repeated_noun: float = 0

        sentences = subflow.sentences
        # skip sentences with 0 or 1 steps, as they do not have a predecessor
        if len(sentences) < 2:
            return -1.0
        else:
            # designate the first step as the initial predecessor
            predecessor: sentence = sentences[0]
            predecessor_nouns: list[str] = predecessor.get_nouns()

            for step in sentences[1:]:
                steps_with_predecessor += 1
                current_nouns: list[str] = step.get_nouns()

                if any(noun in current_nouns for noun in predecessor_nouns):
                    steps_with_repeated_noun += 1

                # update the predecessor for the next iteration
                predecessor = step
                predecessor_nouns: list[str] = predecessor.get_nouns()


        return steps_with_repeated_noun / steps_with_predecessor