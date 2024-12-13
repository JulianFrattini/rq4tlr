from dataclasses import dataclass, field
from util.sentence import sentence

@dataclass
class RawUseCase:
    # a raw, unprocessed use case that simply formats the text files into attributes

    id: int
    name: str = ""
    description: str = ""
    actors: list = field(default_factory=list)
    preconditions: sentence = ""
    postconditions: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    alternative: list[str] = field(default_factory=list)
    quality_requirements: list[str] = field(default_factory=list)

    def __str__(self):
        return f"UseCase(id={self.id}"
    
@dataclass
class UseCase:
    # a processed use case where certain fields that contain sentences have been enriched with syntactic information

    id: int
    name: str = ""
    description: str = ""
    actors: list = field(default_factory=list)
    preconditions: sentence = ""
    postconditions: list[sentence] = field(default_factory=list)
    steps: list[sentence] = field(default_factory=list)
    alternative: list[sentence] = field(default_factory=list)
    quality_requirements: list[sentence] = field(default_factory=list)

    def __str__(self):
        return f"UseCase(id={self.id}"