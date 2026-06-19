from parsers.usecaseparser import AbstractUseCaseParser
from structure.rawusecase import RawUseCase

import re
import spacy

CONJUNCTION_START_PATTERN = re.compile(r"^(and|or|but|nor|so|yet)\b", flags=re.IGNORECASE)
TAG_SPLIT_PATTERN = re.compile(r"(\[[A-Z0-9, ]+\])\s+(The\b.*)$")
TAG_AT_END_PATTERN = re.compile(r"\.\[[A-Z0-9, ]+\]$")
TAG_ONLY_SENTENCE_PATTERN = re.compile(r"^\[[A-Z0-9, ]+\]\.$")
NUMERIC_PAREN_END_PATTERN = re.compile(r"\b\d+\)$")
WORD_PATTERN = re.compile(r"\b\w+\b")
GLOSSARY_TAIL_PATTERN = re.compile(r"^[A-Z][A-Za-z0-9/&\-]*(?:\s+[A-Za-z0-9/&\-]+){0,3}\)")

class ItrustParser(AbstractUseCaseParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def _word_count(self, text: str) -> int:
        return len(WORD_PATTERN.findall(text))

    def _should_merge_with_previous(self, previous: str, current: str) -> bool:
        prev = previous.strip()
        cur = current.strip()
        if not prev or not cur:
            return False

        # Minimal corpus-specific merge rules for obvious line-wrap artifacts.
        if cur.startswith('['):
            if TAG_ONLY_SENTENCE_PATTERN.match(cur) and NUMERIC_PAREN_END_PATTERN.search(prev):
                return False
            return True

        if prev.endswith('/'):
            return True
        if prev.endswith('.') and ')' in cur and self._word_count(cur) <= 6 and GLOSSARY_TAIL_PATTERN.match(cur):
            return True
        if cur.startswith('('):
            return True
        if prev.endswith(':'):
            return True
        if cur[0].islower():
            return True
        if CONJUNCTION_START_PATTERN.match(cur):
            return True

        return False

    def parse_subflow(self, text: str) -> list[str]:
        # Base segmentation comes from spaCy. A minimal post-process layer merges
        # only the most obvious line-wrap artifacts.
        doc = self.nlp(text)
        steps_raw: list[str] = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        steps: list[str] = []
        for step in steps_raw:
            if len(steps) > 0 and self._should_merge_with_previous(steps[-1], step):
                prev_step = steps[-1]
                cur_step = step
                sep = "" if steps[-1].endswith('/') else " "
                steps[-1] = f"{prev_step}{sep}{cur_step}"
            else:
                steps.append(step)

        normalized_steps: list[str] = []
        for step in steps:
            marker_match = TAG_SPLIT_PATTERN.search(step)
            if marker_match:
                idx = marker_match.start(2)
                left = step[:idx].rstrip()
                right = step[idx:].lstrip()
                if left and right:
                    if left[-1] not in '.!?' and not TAG_AT_END_PATTERN.search(left):
                        left = f"{left}."
                    normalized_steps.append(left)
                    normalized_steps.append(right)
                    continue
            normalized_steps.append(step)

        return normalized_steps

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