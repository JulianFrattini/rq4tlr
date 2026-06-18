from dataclasses import dataclass, field

from structure.usecase import UseCase


@dataclass
class SubFlow:
    parent_uc: UseCase
    flow_id: int
    sentences: list[str]