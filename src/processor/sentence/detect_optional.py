from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectOptional(SentenceProcessor):

    name: str = "optional"
    optional_terms: list[str] = ['possibly', 'eventually', 'optionally', 'if possible', 'if appropriate', 'if needed', 'if necessary', 'if required', 'if applicable', 'if desired', 'if applicable']

    def process(self, sentence: sentence) -> bool:
        """
        Determines, whether the sentence contains an optional phrase or not.
        """

        # determine whether the sentence contains any of the terms listed in optional_terms
        for term in self.optional_terms:
            if term in sentence.literal:
                return True
        return False