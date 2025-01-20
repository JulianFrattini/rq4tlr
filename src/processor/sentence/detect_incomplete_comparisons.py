import spacy
from processor.sentence.sentenceprocessor import SentenceProcessor
from structure.sentence import sentence

class DetectIncompleteComparisons(SentenceProcessor):

    def __init__(self):
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_sm
        self.nlp = spacy.load("en_core_web_sm")

    name: str = "incomplete_comparisons"


    def has_quantified_conjunction(self, token):
        # Check for numerical descriptors or quantifiers in the token's ancestors or children
        return any(
            ancestor.pos_ == "NUM" or any(
                child.pos_ == "NUM" for child in ancestor.children
            )
            for ancestor in token.ancestors
        ) or any(
            child.pos_ == "NUM" or any(
                grandchild.pos_ == "NUM" for grandchild in child.children
            )
            for child in token.children
        )


    def process(self, sentence: sentence) -> bool:
        """
        Detects when a sentence in a requirement includes incomplete comparisons.
        
        :param sentence: the sentence to process

        :return: True if the sentence includes incomplete comparisons, False otherwise
        """
        doc = self.nlp(sentence.literal)
        incomplete_comparisons = []

        for token in doc:
            # Check for comparative adjectives (JJR) or adverbs (RBR)
            if token.tag_ in ["JJR", "RBR"]:  # E.g., "cleaner", "better", "faster"
                # Exclude cases where the comparative is part of a quantified conjunction
                has_quant_conjunction = self.has_quantified_conjunction(token)

                # Check if there is a dependent "than" or "as"
                has_comparison_marker = any(
                    child.text.lower() in ["than", "as"] for child in token.children
                )

                # If no comparison marker and no quantified conjunction exists, it's incomplete
                if not has_comparison_marker and not has_quant_conjunction:
                    return True

        return False

