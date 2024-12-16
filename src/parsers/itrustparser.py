from parsers.usecaseparser import AbstractUseCaseParser
from structure.rawusecase import RawUseCase, RawSubflow

import spacy

class ItrustParser(AbstractUseCaseParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def parse_subflow(self, text: str) -> RawSubflow:
        doc = self.nlp(text)
        steps: list[str] = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        subflow: RawSubFlow = RawSubflow(steps=steps)
        return subflow

    def parse(self, ucid: str, uc_texts: dict[str, str], uc_name: str) -> RawUseCase:
        uc: RawUseCase = RawUseCase(id=ucid, name=uc_name)

        # determine the main flows
        main_flows: list[str] = [ucfile for ucfile in uc_texts.keys() if 'E' not in ucfile]
        alternative_flows: list[str] = [ucfile for ucfile in uc_texts.keys() if 'E' in ucfile]
        
        for flow in main_flows:
            uc.main.append(self.parse_subflow(uc_texts[flow]))
        for flow in alternative_flows:
            uc.alternative.append(self.parse_subflow(uc_texts[flow]))

        return uc