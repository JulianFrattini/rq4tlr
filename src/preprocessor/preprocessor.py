import spacy

from structure.sentence import sentence

class Preprocessor:
    def __init__(self):
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_sm
        self.nlp = spacy.load("en_core_web_sm")

    def preprocess_sentence(self, literal: str) -> sentence:
        """
        Preprocess a sentence by performing all preprocessing steps and creating a sentence object
        
        :param literal: the literal sentence to preprocess
        
        :return: the preprocessed sentence
        """
        # Perform POS tagging
        pos_tagged = self.pos_tagging(literal)

        # Create the sentence object
        preprocessed: sentence = sentence(
            literal=literal, 
            pos_tagged=pos_tagged)
        return preprocessed

    def pos_tagging(self, sentence: str) -> list[tuple[str, str]]:
        doc = self.nlp(sentence)
        sentence_parsed = [(token.text, token.pos_) for token in doc]
        return sentence_parsed
