from structure.usecase import UseCase
import pandas as pd

from processor.uc.ucprocessor import UCProcessor
from processor.uc.detect_happy_ucs import DetectHappyUCs
from processor.uc.calc_large_ucs import CalculateLargeUseCases
from processor.uc.calc_meaningless_actors import CalculateMeaninglessActors

from processor.sentence.sentenceprocessor import SentenceProcessor
from processor.sentence.detect_anaphora import DetectAnaphora
from processor.sentence.detect_optional import DetectOptional

class Processor:

    def __init__(self):
        # setup all available processors on their respective levels
        self.processors_uc: list[UCProcessor] = [
            DetectHappyUCs(),
            CalculateLargeUseCases(),
            CalculateMeaninglessActors()
        ]

        self.processors_subflow: list[SentenceProcessor] = []

        self.processors_sentence: list[SentenceProcessor] = [
            DetectAnaphora(),
            DetectOptional()
        ]

    def apply_processors(self, results: pd.DataFrame, datapoints: list, processors: list) -> pd.DataFrame:
        """Applies a list of processors to a list of datapoints. The processors and datapoints must be on the same level, i.e., if the processors are on use-case level, the datapoints must be use-cases as well.
        
        :param datapoints: the list of datapoints to process
        :param processors: the list of processors to apply
        :return: a DataFrame with the results of the processing"""

        # apply the processors
        for processor in processors:
            results[processor.name] = [processor.process(datapoint) 
                for datapoint in datapoints]

        return results

    def apply_uc_processors(self, ucs: list[UseCase]) -> pd.DataFrame:
        """Applies all registered processors on use-case level to a list of use cases and returns a DataFrame with the results
        
        :param ucs: the list of use cases to process
        
        :return: a DataFrame with the results of the processing
        """

        # prepare a datafrane to store the results
        results = pd.DataFrame(columns=['dataset', 'id'])
        results['dataset'] = [uc.dataset for uc in ucs]
        results['id'] = [uc.id for uc in ucs]

        # apply all processors
        results = self.apply_processors(results, ucs, self.processors_uc)
        return results

    def apply_subflow_processors(self, ucs: list[UseCase]) -> pd.DataFrame:
        # prepare a datafrane to store the results
        results = pd.DataFrame(columns=['dataset', 'uc', 'file'])
        datapoints: list[str] = []
        index = 0
        for uc in ucs:
            for filename in uc.main:
                file = uc.main[filename]
                results.loc[index] = [uc.dataset, uc.id, filename]
                datapoints.append(file)
                index += 1
            for filename in uc.alternative:
                file = uc.alternative[filename]
                results.loc[index] = [uc.dataset, uc.id, filename]
                datapoints.append(file)
                index += 1

        # apply all processors
        results = self.apply_processors(results, datapoints, self.processors_subflow)
        return results

    def apply_sentence_processors(self, ucs: list[UseCase]) -> pd.DataFrame:
        # prepare a datafrane to store the results
        results = pd.DataFrame(columns=['dataset', 'uc', 'file', 'line'])
        datapoints: list[str] = []
        index = 0
        for uc in ucs:
            for filename in uc.main:
                file = uc.main[filename]
                for sentence_index, line in enumerate(file):
                    # prepare an entry for the current data point in the results dataframe
                    results.loc[index] = [uc.dataset, uc.id, filename, sentence_index+1]
                    datapoints.append(line)

                    # increment the index
                    index += 1
            for filename in uc.alternative:
                file = uc.alternative[filename]
                for sentence_index, line in enumerate(file):
                    # prepare an entry for the current data point in the results dataframe
                    results.loc[index] = [uc.dataset, uc.id, filename, sentence_index+1]
                    datapoints.append(line)

                    # increment the index
                    index += 1

        # apply all processors
        results = self.apply_processors(results, datapoints, self.processors_sentence)
        return results
