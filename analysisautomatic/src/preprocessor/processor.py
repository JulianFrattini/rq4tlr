import spacy

class Preprocessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def pos_tagging(self, sentence: str) -> list[tuple[str, str]]:
        doc = self.nlp(sentence)
        sentence_parsed = [(token.text, token.pos_) for token in doc]
        return sentence_parsed
