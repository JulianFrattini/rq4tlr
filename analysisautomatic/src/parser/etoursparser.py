from parser.usecaseparser import AbstractUseCaseParser
from util.uc import RawUseCase

class EtoursParser(AbstractUseCaseParser):
    def parse(self, ucid: str, uc_text: str) -> RawUseCase:
        lines: list[str] = uc_text.split('\n')

        uc: RawUseCase = RawUseCase(id=ucid)

        # flags that are used to determine which section of the use case we are parsing
        is_parsing_steps: bool = False
        is_parsing_postconditions: bool = False
        is_parsing_quality_requirements: bool = False

        for line in lines:
            # parse the single-line metadata of the use case
            if line.startswith('Use case name:'):
                uc.name = line.split(':')[1].strip()
            elif line.startswith('Description:'):
                uc.description = line.split(':')[1].strip()
            elif line.startswith('Participating Actor:'):
                uc.actors.append(line.split(':')[1].strip())
            elif line.startswith('Entry Operator conditions:'):
                uc.preconditions = line.split(':')[1].strip()
            elif line.startswith('Flow of events User System:'):
                is_parsing_steps = True
                continue
            elif line.startswith('Exit conditions:'):
                is_parsing_postconditions = True
                uc.postconditions.append(line.split(':')[1].strip())
            elif line.startswith('Quality requirements:'):
                is_parsing_postconditions = False
                is_parsing_quality_requirements = True

            # parse the steps of the main flow of events
            if is_parsing_steps:
                # check if the line starts with a number to determine if it is a step
                # a number may be followed by a period and then a space
                if line.strip()[0].isdigit():
                    uc.steps.append(' '.join(line.split(' ')[1:]).strip())
                else:
                    is_parsing_steps = False

            # parse the postconditions
            if is_parsing_postconditions:
                # the first postcondition may be on the same line as the keywords "Exit conditions:"
                postcondition: str = line.strip()
                if postcondition.startswith('Exit conditions:'):
                    postcondition = postcondition.split(':')[1].strip()
                uc.postconditions.append(postcondition)

            # parse the quality requirements
            if is_parsing_quality_requirements:
                # some quality requirements are on the same line as the keyword "Quality requirements:"
                quality_requirement: str = line.strip()
                if quality_requirement.startswith('Quality requirements:'):
                    quality_requirement = quality_requirement.split(':')[1].strip()

                    # continue in case no quality requirement follows the keyword 
                    if quality_requirement == '':
                        continue
                    else:
                        quality_requirement = quality_requirement.strip()
                uc.quality_requirements.append(quality_requirement)

        return uc