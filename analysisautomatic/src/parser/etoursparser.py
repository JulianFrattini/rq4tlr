from parser.usecaseparser import AbstractUseCaseParser
from util.uc import UseCase

class EtoursParser(AbstractUseCaseParser):
    def parse(self, ucid: str, uc_text: str) -> UseCase:
        lines: list[str] = uc_text.split('\n')

        uc: UseCase = UseCase(id=ucid)

        for line in lines:
            if line.startswith('Use case name:'):
                uc.name = line.split(': ')[1].strip()
            if line.startswith('Description:'):
                uc.description = line.split(': ')[1].strip()

        return uc