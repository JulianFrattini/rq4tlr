import spacy
from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectStartsWithoutNounPhrase(SentenceProcessor):

    def __init__(self):
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_md
        self.nlp = spacy.load("en_core_web_md")

    name: str = "starts_without_nounphrase"

    def process(self, sentence: sentence) -> bool:
        """
        Detects when a sentence in a requirement does not start with a noun phrase.
        
        :param sentence: the sentence to process

        :return: True if the sentence does not start with a noun phrase, False otherwise
        """
        doc = self.nlp(sentence.literal)

        # Get the first token of the sentence
        first_token = doc[0]

        # Find the first noun phrase (np)
        first_noun_phrase = None
        for np in doc.noun_chunks:
            first_noun_phrase = np
            break  # Take the first noun chunk (noun phrase)

        if not first_noun_phrase:
            return True  # No noun phrase found (unlikely, but just in case)

        if first_token == first_noun_phrase[0]:  # The chunk starts with this token
            return False

        return True
