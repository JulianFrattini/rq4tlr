from dataclasses import fields

import spacy
from preprocessor.preprocessor import Preprocessor

from structure.rawusecase import RawUseCase
from structure.usecase import UseCase

class UseCasePreprocessor:

    def __init__(self):
        self.preprocessor = Preprocessor()
        # Load the English model
        # to utilize the spacy model, run python -m spacy download en_core_web_md
        self.nlp = spacy.load("en_core_web_md")

    def preprocess_use_case(self, raw_use_case: RawUseCase, goldstandards, raw_use_cases: list[RawUseCase]) -> UseCase:
        """
        Preprocesses a raw use case by performing all preprocessing steps and returning a preprocessed use case object

        :param raw_use_case: the use case to preprocess
        :goldstandards: a dictionary of the goldstandards
        :raw_use_cases: a list of the raw use cases
        :return: the preprocessed use case

        """
        # set up the preprocessed use case and copy all attributes that do not change
        preprocessed_use_case = UseCase(
            id=raw_use_case.id,
            dataset=raw_use_case.dataset,
            name=raw_use_case.name,
            description=raw_use_case.description,
            actors=raw_use_case.actors,
            goldstandard=goldstandards[raw_use_case.dataset]
        )

        # preprocess all attributes which are lists of strings
        list_attributes: list[str] = ['preconditions', 'postconditions', 'quality_requirements']
        for attribute in list_attributes:
            setattr(preprocessed_use_case, 
                    attribute, 
                    [self.preprocessor.preprocess_sentence(sentence) 
                     for sentence 
                     in getattr(raw_use_case, attribute)])

        # preprocess the main and alternative subflows
        for subflow_type in ['main', 'alternative']:
            subflows = getattr(raw_use_case, subflow_type)
            preprocessed_subflows = {}
            for key, steps in subflows.items():
                preprocessed_subflows[key] = [self.preprocessor.preprocess_sentence(step) for step in steps]
            setattr(preprocessed_use_case, subflow_type, preprocessed_subflows)


        return preprocessed_use_case