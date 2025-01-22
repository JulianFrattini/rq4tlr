import pytest

from src.processor.subflow.calc_coherence import CalculateCoherence

from src.structure.sentence import sentence

class TestCalcCoherence:

    @pytest.fixture
    def sut(self):
        return CalculateCoherence()

    def test_process_perfect(self, sut):
        subflow: list[sentence] = [
            sentence(
                literal="The user provides a username and password.",
                pos_tagged=[("The", "DET"), ("user", "NOUN"), ("provides", "VERB"), ("a", "DET"), ("username", "NOUN"), ("and", "CCONJ"), ("password", "NOUN"), (".", "PUNCT")]),
            sentence(
                literal="The system checks if the username exists.",
                pos_tagged=[("The", "DET"), ("system", "NOUN"), ("checks", "VERB"), ("if", "SCONJ"), ("the", "DET"), ("username", "NOUN"), ("exists", "VERB"), (".", "PUNCT")]),
            sentence(
                literal="The system checks if the password is correct.",
                pos_tagged=[("The", "DET"), ("system", "NOUN"), ("checks", "VERB"), ("if", "SCONJ"), ("the", "DET"), ("password", "NOUN"), ("is", "AUX"), ("correct", "ADJ"), (".", "PUNCT")]),
            sentence(
                literal="If the password is correct, the user logs in.",
                pos_tagged=[("If", "SCONJ"), ("the", "DET"), ("password", "NOUN"), ("is", "AUX"), ("correct", "ADJ"), (",", "PUNCT"), ("the", "DET"), ("user", "NOUN"), ("logs", "VERB"), ("in", "ADP"), (".", "PUNCT")])
        ]

        result = sut.process(subflow)
        assert result == 1.0

    def test_process_imperfect(self, sut):
        subflow: list[sentence] = [
            sentence(
                literal="The user provides a username and password.",
                pos_tagged=[("The", "DET"), ("user", "NOUN"), ("provides", "VERB"), ("a", "DET"), ("username", "NOUN"), ("and", "CCONJ"), ("password", "NOUN"), (".", "PUNCT")]),
            sentence(
                literal="The system checks if the name exists.",
                pos_tagged=[("The", "DET"), ("system", "NOUN"), ("checks", "VERB"), ("if", "SCONJ"), ("the", "DET"), ("name", "NOUN"), ("exists", "VERB"), (".", "PUNCT")]),
            sentence(
                literal="The system checks if the password is correct.",
                pos_tagged=[("The", "DET"), ("system", "NOUN"), ("checks", "VERB"), ("if", "SCONJ"), ("the", "DET"), ("password", "NOUN"), ("is", "AUX"), ("correct", "ADJ"), (".", "PUNCT")]),
            sentence(
                literal="If the password is correct, the user logs in.",
                pos_tagged=[("If", "SCONJ"), ("the", "DET"), ("password", "NOUN"), ("is", "AUX"), ("correct", "ADJ"), (",", "PUNCT"), ("the", "DET"), ("user", "NOUN"), ("logs", "VERB"), ("in", "ADP"), (".", "PUNCT")])
        ]

        result = sut.process(subflow)
        assert result == (2.0/3.0)

    def test_process_none(self, sut):
        subflow: list[sentence] = [
            sentence(
                literal="The user provides a username and password.",
                pos_tagged=[("The", "DET"), ("user", "NOUN"), ("provides", "VERB"), ("a", "DET"), ("username", "NOUN"), ("and", "CCONJ"), ("password", "NOUN"), (".", "PUNCT")]),
            sentence(
                literal="The system checks if the name exists.",
                pos_tagged=[("The", "DET"), ("system", "NOUN"), ("checks", "VERB"), ("if", "SCONJ"), ("the", "DET"), ("name", "NOUN"), ("exists", "VERB"), (".", "PUNCT")]),
            sentence(
                literal="The frontend checks if the password is correct.",
                pos_tagged=[("The", "DET"), ("frontend", "NOUN"), ("checks", "VERB"), ("if", "SCONJ"), ("the", "DET"), ("password", "NOUN"), ("is", "AUX"), ("correct", "ADJ"), (".", "PUNCT")])
        ]

        result = sut.process(subflow)
        assert result == 0.0