from processor.uc.ucprocessor import UCProcessor
from structure.usecase import UseCase

class CalculateMeaninglessActors(UCProcessor):

    name: str = "meaningless_actor"

    def process(self, uc: UseCase) -> int:
        """
        Counts the number of meaningless actors, i.e., actors that do not appear in the use case description.
        
        :param uc: the use case to process

        :return: True if the use case is happy, False otherwise
        """
        # by default, assume all actors to be meaningless
        meaningless_actors: list[str] = uc.actors.copy()

        # remove actors from the list if they appear at least once in any of the main subflows
        for step in uc.main.values():
            for actor in uc.actors:
                if actor in step:
                    meaningless_actors.remove(actor)
        # remove actors from the list if they appear at least once in any of the alternative subflows
        for step in uc.alternative.values():
            for actor in uc.actors:
                if actor in step:
                    meaningless_actors.remove(actor)

        # return the number of remaining, meaningless actors
        return len(meaningless_actors)