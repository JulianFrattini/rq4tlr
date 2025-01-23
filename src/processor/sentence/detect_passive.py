from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

import spacy
from spacy.matcher import Matcher

class DetectPassive(SentenceProcessor):

    name: str = "passive"

    def __init__(self):
        passive_rules = [
            [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}],
            [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBZ'}],
            [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'RB'}, {'TAG': 'VBN'}],
        ]

        nlp = spacy.load('en_core_web_md')
        self.matcher = Matcher(nlp.vocab)
        self.matcher.add('Passive',  passive_rules)

    def process(self, sentence: sentence) -> bool:
        """
        Determines, whether the sentence is written in passive voice or not
        """

        matches = self.matcher(sentence.doc)
        if len(matches) > 0:
            return True
        return False