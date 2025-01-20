import spacy
from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectStartsWithoutSubject(SentenceProcessor):

    def __init__(self):
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_sm
        self.nlp = spacy.load("en_core_web_sm")

    name: str = "starts_without_subject"

    def process(self, sentence: sentence) -> bool:
        """
        Detects when a sentence in a requirement does not start with the subject.
        
        :param sentence: the sentence to process

        :return: True if the sentence does not start with the subject, False otherwise
        """
        doc = self.nlp(sentence.literal)

        # Find the first noun phrase (np)
        first_noun_phrase = None
        for np in doc.noun_chunks:
            first_noun_phrase = np
            break  # Take the first noun chunk (noun phrase)

        if not first_noun_phrase:
            return True  # No noun phrase found (unlikely, but just in case)

        # Check if the subject is part of the first noun phrase
        for token in doc:
            # Look for the subject (subject could be a noun or a pronoun)
            if "subj" in token.dep_:
                if token in first_noun_phrase:
                    return False  # Subject is within the first noun phrase
                else:
                    return True  # Subject is outside the first noun phrase

        return True  # No subject found
