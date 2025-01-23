import spacy

from structure.sentence import sentence

class Preprocessor:
    def __init__(self):
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_md
        self.nlp = spacy.load("en_core_web_md")

    def preprocess_sentence(self, literal: str) -> sentence:
        """
        Preprocess a sentence by performing all preprocessing steps and creating a sentence object
        
        :param literal: the literal sentence to preprocess
        
        :return: the preprocessed sentence
        """
        # preprocess the sentence
        doc = self.nlp(literal)

        # Create the sentence object
        preprocessed: sentence = sentence(
            literal=literal, 
            pos_tagged=[(token.text, token.pos_) for token in doc],
            doc=doc)
        return preprocessed
