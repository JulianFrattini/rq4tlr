from dataclasses import dataclass, field
from structure.sentence import sentence

from structure.TLR_goldstandard import TLR_goldstandard


@dataclass
class UseCase:
    # a processed use case where certain fields that contain sentences have been enriched with syntactic information
    
    id: int
    dataset: str
    name: str = ""
    description: str = ""
    actors: list = field(default_factory=list)

    preconditions: list[sentence] = field(default_factory=list)
    postconditions: list[sentence] = field(default_factory=list)

    main: dict[str, list[sentence]] = field(default_factory=dict)
    alternative: dict[str, list[sentence]] = field(default_factory=dict)

    quality_requirements: list[sentence] = field(default_factory=list)

    goldstandard: TLR_goldstandard = field(default_factory=TLR_goldstandard)

    similarities: dict[str, float] = field(default_factory=dict)