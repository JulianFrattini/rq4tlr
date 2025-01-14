from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class CalcRequirementsLength(SentenceProcessor):

    name: str = "requirements_length"

    def process(self, sentence: sentence) -> bool:
        """
        Determines the length of a requirement in number of words.
        """
        return len(sentence.pos_tagged)