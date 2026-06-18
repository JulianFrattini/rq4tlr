from parsers.usecaseparser import AbstractUseCaseParser
from structure.rawusecase import RawUseCase

import spacy

class ItrustParser(AbstractUseCaseParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")

    def parse_subflow(self, text: str) -> list[str]:
        doc = self.nlp(text)
        steps: list[str] = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        return steps

    def parse(self, ucid: str, uc_texts: dict[str, str], uc_name: str) -> RawUseCase:
        uc: RawUseCase = RawUseCase(id=ucid, dataset="itrust", name=uc_name)

        # determine the main flows
        main_flows: list[str] = sorted([ucfile for ucfile in uc_texts.keys() if 'E' not in ucfile])
        alternative_flows: list[str] = sorted([ucfile for ucfile in uc_texts.keys() if 'E' in ucfile])
                
        # parse the main sub flows
        for flow in main_flows:
            # parse the steps of the subflow
            subflow: list[str] = self.parse_subflow(uc_texts[flow])
            # determine the filename that contained the subflow
            filename: str = flow.split('.')[0]
            # store the subflow in the main subflows of the use case
            uc.main[filename] = subflow

        # parse the alternative sub flows
        for flow in alternative_flows:
            subflow: list[str] = self.parse_subflow(uc_texts[flow])
            filename: str = flow.split('.')[0]
            uc.alternative[filename] = subflow

        return uc