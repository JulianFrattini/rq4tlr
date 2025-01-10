from dataclasses import dataclass, field
from dataclasses import asdict

@dataclass
class RawUseCase:
    # a raw, unprocessed use case that simply formats the text files into attributes

    id: int
    dataset: str = ""
    name: str = ""
    description: str = ""
    actors: list = field(default_factory=list)

    preconditions: list[str] = field(default_factory=list)
    postconditions: list[str] = field(default_factory=list)

    # subflows of the use case, where each use case can contain multiple main and alternative subflows
    # the two attributes main and alternative consist of a mapping for filenames (e.g., UC1S2) to a list of subflow steps
    main: dict[str, list[str]] = field(default_factory=dict)
    alternative: dict[str, list[str]] = field(default_factory=dict)

    quality_requirements: list[str] = field(default_factory=list)

    def __str__(self):
        return f"UseCase(id={self.id}"

    def to_dict(self) -> dict:
        return asdict(self)