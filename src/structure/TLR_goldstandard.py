from dataclasses import dataclass, field

@dataclass
class TLR_goldstandard:
    # a dataclass for holding the goldstandard trace link information for a dataset

    dataset: str
    links: dict[str] = field(default_factory=list)
