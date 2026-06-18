from parsers.usecaseparser import AbstractUseCaseParser
from structure.rawusecase import RawUseCase

import re
import spacy

BRACKET_HEAD_PATTERN = re.compile(r"^\[([^\]]+)\](.*)$", flags=re.DOTALL)
CONJUNCTION_START_PATTERN = re.compile(r"^(and|or|but|nor|so|yet)\b", flags=re.IGNORECASE)
BRACKET_TAIL_KEYWORD_START_PATTERN = re.compile(r"^(the|and|or)\b", flags=re.IGNORECASE)
ID_START_PATTERN = re.compile(r"^id\b", flags=re.IGNORECASE)
PAREN_CONTINUATION_PATTERN = re.compile(r"^\([^)]+\)\s+(and|or)\b", flags=re.IGNORECASE)
WORD_PATTERN = re.compile(r"\b\w+\b")
TAG_SPLIT_PATTERN = re.compile(r"(\[[A-Z0-9, ]+\])\s+(The\b.*)$")
TAG_AT_END_PATTERN = re.compile(r"\.\[[A-Z0-9, ]+\]$")
COLON_NEWLINE_THE_PATTERN = re.compile(r":\s*\n\s*(The\b)")
DOT_PAREN_AND_OR_PATTERN = re.compile(r"\.\s+(\([^)]+\)\s+(?:and|or)\b)")
LOWERCASE_WORD_END_PATTERN = re.compile(r"\b[a-z]+$")
ALNUM_END_PATTERN = re.compile(r"[A-Za-z0-9]$")

class ItrustParser(AbstractUseCaseParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")

    def _word_count(self, text: str) -> int:
        return len(WORD_PATTERN.findall(text))

    def _is_satisfaction_question_pair(self, previous: str, current: str) -> bool:
        prev = previous.lower()
        cur = current.lower()
        return (
            previous.endswith('?')
            and current.endswith('?')
            and prev.startswith('how ')
            and cur.startswith('how ')
            and 'satisfied' in prev
            and 'satisfied' in cur
        )

    def _normalize_step(self, step: str) -> list[str]:
        # These step-level normalizations are derived from a manual pass over parser output
        # where spaCy sentence boundaries did not align with the shipped iTrust formatting.
        cleaned = step
        # Normalize wrapped heading continuations like ":\nThe ..." into a single sentence.
        cleaned = COLON_NEWLINE_THE_PATTERN.sub(r": \1", cleaned)
        # Keep parenthetical continuations inline when a splitter inserts an extra period.
        cleaned = DOT_PAREN_AND_OR_PATTERN.sub(r" \1", cleaned)

        # Split fused markers where a new sentence starts after a tag.
        marker_match = TAG_SPLIT_PATTERN.search(cleaned)
        if marker_match:
            idx = marker_match.start(2)
            left = cleaned[:idx].rstrip()
            right = cleaned[idx:].lstrip()
            if left and right:
                if left[-1] not in '.!?' and not TAG_AT_END_PATTERN.search(left):
                    left = f"{left}."
                return [left, right]

        return [cleaned]

    def _should_merge_with_previous(self, previous: str, current: str) -> bool:
        prev = previous.strip()
        cur = current.strip()
        if not prev or not cur:
            return False

        # Merge heuristics below were introduced after manual inspection of generated
        # iTrust outputs. They compensate for known spaCy split artifacts so that parsed
        # subflows retain the intended sentence granularity from shipped artifacts.

        # Keep bracket tags attached when they are a suffix marker or inline continuation,
        # but do not merge if the tag begins a clearly new sentence.
        if cur.startswith('['):
            match = BRACKET_HEAD_PATTERN.match(cur)
            if match:
                tag = match.group(1)
                tail = match.group(2).lstrip()
                if tail in {"", "."}:
                    if tail == "." and "," in tag:
                        return bool(ALNUM_END_PATTERN.search(prev))
                    return True
                if tail and (tail[0].islower() or tail[0] in ",;:"):
                    return True
                if tail.startswith('('):
                    return True
                if BRACKET_TAIL_KEYWORD_START_PATTERN.match(tail):
                    return True
            # Handle malformed/open bracket continuations in wrapped lines.
            if ']' not in cur and prev[-1] not in '.!?':
                return True

        # Common line-wrap continuation patterns from the iTrust corpus.
        if prev.endswith('/'):
            return True
        if cur[0].islower():
            return True
        if CONJUNCTION_START_PATTERN.match(cur):
            return True

        # Keep this heading/list continuation inline.
        if prev.endswith(':') and cur.startswith('The sender'):
            return True
        if prev.lower().endswith('following:') and ':' in cur:
            return True

        # Keep short parenthetical glossary tails together when a definition is still open.
        if (
            prev.count('(') > prev.count(')')
            and ')' in cur
            and self._word_count(cur) <= 5
        ):
            return True

        # Keep line-wrap artifacts like "hospital" + "Id number ..." together.
        if ID_START_PATTERN.match(cur) and LOWERCASE_WORD_END_PATTERN.search(prev):
            return True

        # Keep parenthetical continuation blocks like "(In ...) and ..." inline.
        if PAREN_CONTINUATION_PATTERN.match(cur):
            return True

        return False

    def parse_subflow(self, text: str) -> list[str]:
        # Base segmentation comes from spaCy, then deterministic adaptation rules are
        # applied because raw spaCy sentence boundaries are not consistently valid for
        # the iTrust corpus (as established by manual output review).
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
            normalized_steps.extend(self._normalize_step(step))

        merged_steps: list[str] = []
        for step in normalized_steps:
            if len(merged_steps) > 0 and self._is_satisfaction_question_pair(merged_steps[-1], step):
                merged_steps[-1] = f"{merged_steps[-1]}\n{step}"
            else:
                merged_steps.append(step)

        return merged_steps

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