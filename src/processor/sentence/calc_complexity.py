from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class CalcComplexity(SentenceProcessor):

    name: str = "sentence_complexity"

    def process(self, sentence: sentence) -> bool:
        """
        Calculate the number of noun chunks as a heuristic for sentence complexity
        """
        return len(list(sentence.doc.noun_chunks))