from preprocessor.preprocessor import Preprocessor

from util.uc import RawUseCase, UseCase

class UseCasePreprocessor:

    def __init__(self):
        self.preprocessor = Preprocessor()

    def preprocess_use_case(self, raw_use_case: RawUseCase) -> UseCase:
        """
        Preprocesses a raw use case by performing all preprocessing steps and returning a preprocessed use case object

        :param raw_use_case: the use case to preprocess
        :return: the preprocessed use case
        """
        # set up the preprocessed use case and copy all attributes that do not change
        preprocessed_use_case = UseCase(
            id=raw_use_case.id,
            name=raw_use_case.name,
            description=raw_use_case.description)

        # preprocess all single sentences
        sentence_attributes: list[str] = ['preconditions']
        for attribute in sentence_attributes:
            setattr(preprocessed_use_case, 
                    attribute, 
                    self.preprocessor.preprocess_sentence(
                        getattr(raw_use_case, attribute)))

        # preprocess the lists of sentences
        list_attributes: list[str] = ['actors', 'postconditions', 'steps', 'alternative', 'quality_requirements']
        for attribute in list_attributes:
            setattr(preprocessed_use_case, 
                    attribute, 
                    [self.preprocessor.preprocess_sentence(sentence) 
                     for sentence 
                     in getattr(raw_use_case, attribute)])

        return preprocessed_use_case