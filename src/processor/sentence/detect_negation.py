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
        for token in sentence.doc:
            if token.text in ['not', "n't", "wouldn't", 'never', 'nowhere', 'noone', 'no-one']:
                if token.dep_ == 'neg' and (token.head.pos_ == 'VERB' or token.head.pos_ == 'AUX'):
                    return True
        return False