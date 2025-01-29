from structure.usecase import UseCase
from util.static import LEVELS
import pandas as pd

from processor.uc.ucprocessor import UCProcessor
from processor.uc.detect_happy_ucs import DetectHappyUCs
from processor.uc.calc_large_ucs import CalculateLargeUseCases
from processor.uc.calc_meaningless_actors import CalculateMeaninglessActors
from processor.uc.detect_meaningless_uc import DetectMeaninglessUC
from processor.uc.detect_scattered_requirements import DetectScatteredRequirements
from processor.uc.detect_tangled_requirements import DetectTangledRequirements
from processor.uc.detect_nfrs import DetectNonFunctionalRequirements

from processor.subflow.subflowprocessor import SubflowProcessor
from processor.subflow.calc_coherence import CalculateCoherence

from processor.sentence.sentenceprocessor import SentenceProcessor
from processor.sentence.detect_anaphora import DetectAnaphora
from processor.sentence.detect_optional import DetectOptional
from processor.sentence.calc_requirements_length import CalcRequirementsLength
from processor.sentence.detect_incomplete_comparisons import DetectIncompleteComparisons
from processor.sentence.detect_starts_without_subject import DetectStartsWithoutSubject
from processor.sentence.detect_passive import DetectPassive


class Processor:

    def __init__(self):
        self.processors: dict[str, list] = {
            LEVELS[0] : [ # use case level
                DetectHappyUCs(),
                CalculateLargeUseCases(),
                CalculateMeaninglessActors(),
                DetectMeaninglessUC(),
                DetectTangledRequirements(),
                DetectScatteredRequirements(),
                DetectNonFunctionalRequirements()
            ], 
            LEVELS[1] : [ # subflow level
                CalculateCoherence()
            ],
            LEVELS[2] : [ # sentence level
                DetectAnaphora(),
                DetectOptional(),
                CalcRequirementsLength(),
                DetectStartsWithoutSubject(),
                DetectIncompleteComparisons(),
                DetectPassive()
            ]
        }

    def apply_processors(self, level: str, ucs: list[UseCase]) -> pd.DataFrame:

        datapoints: list = []
        results: pd.DataFrame = None
        if level == LEVELS[0]:
            datapoints, results = self.setup_data_ucs()
        elif level == LEVELS[1]:
            datapoints, results = self.setup_data_subflow(ucs)
        elif level == LEVELS[2]:
            datapoints, results = self.setup_data_sentence(ucs)

        # apply the processors
        for processor in self.processors[level]:
            results[processor.name] = [processor.process(datapoint) 
                for datapoint in datapoints]

        return results

    def setup_data_ucs(self, ucs: list[UseCase]) -> pd.DataFrame:
        # prepare a datafrane to store the results
        results = pd.DataFrame(columns=['dataset', 'id'])
        results['dataset'] = [uc.dataset for uc in ucs]
        results['id'] = [uc.id for uc in ucs]

        return ucs, results

    def setup_data_subflow(self, ucs: list[UseCase]) -> pd.DataFrame:
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

        return datapoints, results

    def setup_data_sentence(self, ucs: list[UseCase]) -> pd.DataFrame:
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

        return datapoints, results
