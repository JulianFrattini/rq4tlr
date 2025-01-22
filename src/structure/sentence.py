from dataclasses import dataclass, field

@dataclass
class sentence:

    # the literal sentence
    literal: str = ""

    # list of tuples with the word and its part of speech
    pos_tagged: list = field(default_factory=list)

    def get_nouns(self) -> list[str]:
        """
        Get the nouns from the sentence
        """
        return [word for word, pos in self.pos_tagged if pos.startswith("N")]