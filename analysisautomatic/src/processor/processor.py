from processor.absprocessor import AbsProcessor

from util.uc import UseCase
import pandas as pd

from processor.detect_happy_ucs import DetectHappyUCs
from processor.calc_large_ucs import CalculateLargeUseCases

class Processor:

    def __init__(self):
        # setup all available processors
        self.processors: list[AbsProcessor] = [
            DetectHappyUCs(),
            CalculateLargeUseCases()
        ]

    def apply_processors(self, ucs: list[UseCase]) -> pd.DataFrame:
        """Applies all registered processors to a list of use cases and returns a DataFrame with the results
        
        :param ucs: the list of use cases to process
        
        :return: a DataFrame with the results of the processing
        """

        # create a new dataframe to store the results and insert the ids of each use case from the ucs list
        results = pd.DataFrame(columns=['id'])
        results['id'] = [uc.id for uc in ucs]

        # apply each processor to each use case

        for processor in self.processors:
            results[processor.name] = [processor.process(uc) for uc in ucs]

        # return the results
        return results