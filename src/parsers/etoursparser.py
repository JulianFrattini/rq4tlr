from parsers.usecaseparser import AbstractUseCaseParser
from structure.rawusecase import RawUseCase

class EtoursParser(AbstractUseCaseParser):
    def parse(self, ucid: str, uc_texts: dict[str, str]) -> RawUseCase:
        # in the eTours data set, every use case is contained in one single text file
        uc_file: str = list(uc_texts.keys())[0].split('.')[0]
        uc_text: str = list(uc_texts.values())[0]
        lines: list[str] = uc_text.split('\n')

        uc: RawUseCase = RawUseCase(id=ucid, dataset="etour")

        # flags that are used to determine which section of the use case we are parsing
        is_parsing_steps: bool = False
        subflow: list[str] = []
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
            elif line.startswith('Quality requirements:'):
                is_parsing_postconditions = False
                is_parsing_quality_requirements = True

            # parse the steps of the main flow of events
            if is_parsing_steps:
                # check if the line starts with a number to determine if it is a step
                # a number may be followed by a period and then a space
                if line.strip()[0].isdigit():
                    step: str = ' '.join(line.split(' ')[1:]).strip()
                    subflow.append(step)
                else:
                    # add the one subflow to the main flow of the use case
                    uc.main[uc_file] = subflow
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

                # append the quality requirement if it is non empty
                if quality_requirement != '':
                    uc.quality_requirements.append(quality_requirement)

        return uc