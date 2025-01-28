import pytest

from src.processor.uc.detect_nfrs import DetectNonFunctionalRequirements

from src.structure.usecase import UseCase

class TestDetectNFRs:

    @pytest.fixture
    def sut(self):
        return DetectNonFunctionalRequirements()

    def test_contains_nfrs(self, sut):
        uc = UseCase(
            id=1,
            dataset="eTour",
            name="Test",
            description="Test",
            actors=[],
            preconditions=[],
            postconditions=[],
            main=[],
            alternative=[],
            quality_requirements=["Test"],
            goldstandard=None
        )

        result = sut.process(uc)
        assert result == True

    def test_contains_no_nfrs(self, sut):
        uc = UseCase(
            id=2,
            dataset="eTour",
            name="Test",
            description="Test",
            actors=[],
            preconditions=[],
            postconditions=[],
            main=[],
            alternative=[],
            quality_requirements=[],
            goldstandard=None
        )

        result = sut.process(uc)
        assert result == False