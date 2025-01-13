from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectAnaphora(SentenceProcessor):

    name: str = "anaphora"

    def process(self, sentence: sentence) -> bool:
        """
        Determines, whether the sentence contains a pronoun or not
        """
        return False