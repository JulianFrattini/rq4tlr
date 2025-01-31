from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectAnaphora(SentenceProcessor):

    name: str = "anaphora"

    def process(self, sentence: sentence) -> bool:
        """
        Determines, whether the sentence contains an ambiguous anaphora or not
        """
        doc = sentence.doc

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