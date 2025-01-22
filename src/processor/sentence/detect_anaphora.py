import spacy
from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectAnaphora(SentenceProcessor):

    def __init__(self):
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_md
        self.nlp = spacy.load("en_core_web_md")

    name: str = "anaphora"

    def process(self, sentence: sentence) -> bool:
        """
        Determines, whether the sentence contains an ambiguous anaphora or not
        """
        # Process the sentence with spaCy
        doc = self.nlp(sentence.literal)

        # Identify noun phrases and pronouns
        noun_phrases = [chunk for chunk in doc.noun_chunks]
        pronouns = [token for token in doc if token.pos_ == "PRON"]

        # Find potential coreferent links (based on proximity and dependency)
        ambiguous_corefs = []
        for pronoun in pronouns:
            # Potential antecedents are noun phrases in the same sentence
            potential_antecedents = [
                np.text for np in noun_phrases
                if np.start < pronoun.i  # Noun phrase occurs before the pronoun
            ]
            # Check for ambiguity (more than one antecedent)
            return len(potential_antecedents) > 1

        return False