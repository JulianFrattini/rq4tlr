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
        # Initialize the similarity cache as a dictionary
        self.similarity_cache = {}
        self.joined_string_cache = {}

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
            goldstandard=goldstandards[raw_use_case.dataset],
            similarities=self.calculate_similarities(raw_use_case, raw_use_cases)
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

    def calculate_similarities(self, raw_use_case: RawUseCase, raw_use_cases: list[RawUseCase]) -> dict:
        """
        Calculate similarities between a given use case and a list of use cases.

        Args:
            raw_use_case (RawUseCase): The primary use case for which similarities are being calculated.
            raw_use_cases (list[RawUseCase]): A list of use cases to compare against.

        Returns:
            dict: A dictionary where keys are the IDs of the compared use cases and values are the similarity scores.
        """
        similarities = {}  # Initialize a dictionary to store similarity results.

        # Check if the joined string for the primary use case is already cached.
        if raw_use_case.id in self.joined_string_cache:
            joined_string = self.joined_string_cache[raw_use_case.id]
        else:
            # Generate the joined string and cache it for future use.
            joined_string = self.join_fields(raw_use_case)
            self.joined_string_cache[raw_use_case.id] = joined_string

        # Create a SpaCy document for the primary use case.
        doc1 = self.nlp(joined_string)

        # Iterate over all other use cases to calculate similarities.
        for use_case in raw_use_cases:
            if use_case.id != raw_use_case.id:  # Avoid comparing a use case with itself.
                # Check if the similarity between these two use cases is already cached.
                if self.has_similarity(raw_use_case.id, use_case.id):
                    # Retrieve the cached similarity value.
                    similarities[use_case.id] = self.retrieve(raw_use_case.id, use_case.id)
                else:
                    # Check if the joined string for the current use case is cached.
                    if use_case.id in self.joined_string_cache:
                        joined_string_other = self.joined_string_cache[use_case.id]
                    else:
                        # Generate the joined string and cache it.
                        joined_string_other = self.join_fields(use_case)
                        self.joined_string_cache[use_case.id] = joined_string_other

                    # Create a SpaCy document for the current use case.
                    doc2 = self.nlp(joined_string_other)

                    # Calculate similarity between the two documents.
                    similarities[use_case.id] = doc1.similarity(doc2)

                    # Store the calculated similarity in the cache for future use.
                    self.store(raw_use_case.id, use_case.id, similarities[use_case.id])

        # Return the dictionary of similarities.
        return similarities

    def join_fields(self, use_case: RawUseCase, delimiter="\n") -> str:
        """
        Joins various fields of a use case into a single string, separated by a specified delimiter.

        Args:
            use_case (RawUseCase): The use case object containing the fields to join.
            delimiter (str, optional): The string used to separate fields in the output. Defaults to "\n".

        Returns:
            str: A single string containing all joined fields of the use case.
        """
        # Start with the use case name.
        joined = use_case.name

        # Add the description field, separated by the delimiter.
        joined = delimiter.join([joined, use_case.description])

        # Add all actor names, each separated by the delimiter.
        for actor in use_case.actors:
            joined = delimiter.join([joined, actor])

        # Add all preconditions, each separated by the delimiter.
        for precondition in use_case.preconditions:
            joined = delimiter.join([joined, precondition])

        # Add all steps from the main flow, organized by flow name.
        for flow in use_case.main:
            for step in use_case.main[flow]:
                joined = delimiter.join([joined, step])

        # Add all steps from the alternative flow, organized by flow name.
        for flow in use_case.alternative:
            for step in use_case.alternative[flow]:
                joined = delimiter.join([joined, step])

        # Add all postconditions, each separated by the delimiter.
        for postcondition in use_case.postconditions:
            joined = delimiter.join([joined, postcondition])

        # Add all quality requirements, each separated by the delimiter.
        for quality_requirement in use_case.quality_requirements:
            joined = delimiter.join([joined, quality_requirement])

        # Return the fully joined string.
        return joined

    def _make_key(self, id1, id2):
        """Create a sorted tuple as the key to ensure id1, id2 == id2, id1"""
        return tuple(sorted((id1, id2)))

    def store(self, id1, id2, similarity):
        """Store the similarity between two IDs."""
        key = self._make_key(id1, id2)
        self.similarity_cache[key] = similarity

    def retrieve(self, id1, id2):
        """Retrieve the similarity between two IDs, or return None if not found."""
        key = self._make_key(id1, id2)
        return self.similarity_cache.get(key)

    def has_similarity(self, id1, id2):
        """Check if a similarity value exists between two IDs."""
        key = self._make_key(id1, id2)
        return key in self.similarity_cache