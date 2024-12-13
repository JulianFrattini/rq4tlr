from dataclasses import dataclass, field
from dataclasses import asdict

@dataclass
class RawUseCase:
    # a raw, unprocessed use case that simply formats the text files into attributes

    id: int
    name: str = ""
    description: str = ""
    actors: list = field(default_factory=list)

    preconditions: list[str] = field(default_factory=list)
    postconditions: list[str] = field(default_factory=list)

    steps: list[str] = field(default_factory=list)
    alternative: list[str] = field(default_factory=list)

    quality_requirements: list[str] = field(default_factory=list)

    def __str__(self):
        return f"UseCase(id={self.id}"

    def to_dict(self) -> dict:
        return asdict(self)