from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectNegation(SentenceProcessor):

    name: str = "negation"

    def process(self, sentence: sentence) -> bool:
        """
        Determines, whether a sentence contains a negation or not.
        """
        
        for e in sentence.doc.ents:
            if e._.negex:
                return True
        return False