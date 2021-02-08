import re
import logging
import typer
from pprint import pformat
from functools import reduce
from tqdm import tqdm
from jsonsempai import magic
from model import Model
from beautifultable import BeautifulTable
import holmes_extractor as holmes
import patches.holmes_extractor.semantics as semantics
import ChatbotCorpus
from textdistance import cosine


logger = logging.getLogger("holmes_extractor")
logger.setLevel(logging.DEBUG)
h = logging.FileHandler("holmes_extractor.log")
f = logging.Formatter("[%(asctime)s] - %(message)s")
h.setFormatter(f)
logger.addHandler(h)


# patch semantic analyzer
holmes.semantics.EnglishSemanticAnalyzer = semantics.PatchedEnglishSemanticAnalyzer

MD_MODEL_NAME = "en_core_web_md"
LG_MODEL_NAME = "en_core_web_lg"
NUM_RETURN_SEQUENCES = 10
ENTITIES = [
    "ENTITYNOUN",
    "ENTITYPERSON",
    "ENTITYNORP",
    "ENTITYFAC",
    "ENTITYORG",
    "ENTITYGPE",
    "ENTITYLOC",
    "ENTITYPRODUCT",
    "ENTITYEVENT",
    "ENTITYWORK_OF_ART",
    "ENTITYLAW",
    "ENTITYLANGUAGE",
    "ENTITYDATE",
    "ENTITYTIME",
    "ENTITYPERCENT",
    "ENTITYMONEY",
    "ENTITYQUANTITY",
    "ENTITYORDINAL",
    "ENTITYCARDINAL",
]


class Matcher:
    def __init__(
        self,
        model,
        overall_similarity_threshold=1.0,
        embedding_based_matching_on_root_words=False,
        analyze_derivational_morphology=True,
        perform_coreference_resolution=None,
        debug=False,
    ):
        self.manager = holmes.Manager(
            model=model,
            ontology=None,
            overall_similarity_threshold=overall_similarity_threshold,
            embedding_based_matching_on_root_words=embedding_based_matching_on_root_words,
            analyze_derivational_morphology=analyze_derivational_morphology,
            perform_coreference_resolution=perform_coreference_resolution,
            debug=debug,
        )

    def match_phrase(self, search_phrases, phrase):
        for sp in search_phrases:
            self.manager.register_search_phrase(sp)
        return self.manager.match_search_phrases_against(entry=phrase)


def is_match(phrase1, phrase2, threshold=0.75):
    similarity = cosine.normalized_similarity(phrase1, phrase2)

    return (similarity >= threshold)

def check_result(results, all_matches, threshold=0.75):
    res = []
    for result in results:
        matches = result.get("word_matches", [])
        if not matches:
            continue

        res.append(
            any(
                [
                    is_match(
                        " ".join(
                            [
                                m["search_phrase_word"].lower()
                                for m in matches
                            ]
                        ),
                        match.lower(),
                        threshold=threshold
                    ) for match in all_matches
                ]
            )
        )

    return any(res)


def find_ids(id_text, s):
    r = rf"".join([rf"\s*{c}" for c in id_text])
    return re.findall(rf"{r}\s*", s, re.IGNORECASE)


def check_entities(src_phrase, dst_phrase):
    def make_reducer(phrase):
        def _reducer(a, v):
            a.extend(find_ids(v, phrase))
            return a

        return _reducer

    src_ents = reduce(make_reducer(src_phrase), ENTITIES, [])
    dst_raw_ents = reduce(make_reducer(dst_phrase), ENTITIES, [])
    normalized = dst_phrase
    for e in dst_raw_ents:
        normalized = (
            normalized.replace(e, f' {e.replace(" ", "").upper()} ')
            .replace(" .", ".")
            .replace(".  ", ". ")
            .replace(" ?", "?")
            .replace("?  ", "? ")
        )
    dst_ents = [e.replace(" ", "").upper() for e in dst_raw_ents]
    return sorted([e.strip() for e in src_ents]) == sorted(dst_ents), normalized


def create_paraphrases(model, phrases):
    result = []
    for phrase in phrases:
        result.append(phrase)
        for p in model.run(phrase, NUM_RETURN_SEQUENCES):
            valid, normalized = check_entities(phrase, p)
            if valid:
                result.append(normalized)
    return result


def main(paraphrase_search_phrases: bool = False, paraphrase_input: bool = False, large_model: bool = False, sentences: int = 0, threshold: float = 0.75):
    model = None
    if paraphrase_search_phrases or paraphrase_input:
        model = Model("tuner007/pegasus_paraphrase")
        model.prepare()

    logger.info("-" * 120)
    success, count, errors, non_empty_count = 0, 0, 0, 0
    model_name = LG_MODEL_NAME if large_model else MD_MODEL_NAME
    logger.info(f"Using {model_name} model")
    matcher = Matcher(model_name)
    sent_iter = (
        ChatbotCorpus.sentences
        if not sentences
        else ChatbotCorpus.sentences[:sentences]
    )
    for sentence in tqdm(sent_iter):
        if paraphrase_search_phrases:
            search_phrases = create_paraphrases(model, sentence.templates)
        else:
            search_phrases = sentence.templates

        for input_ in sentence.inputs:
            inp_phrases = create_paraphrases(model, [input_]) if paraphrase_input else [input_]
            found = False
            for inp in inp_phrases:
                try:
                    result = matcher.match_phrase(search_phrases, inp)
                    if result:
                        non_empty_count += 1
                        logger.debug(f"Non-empty result found: {pformat(result)}")
                except Exception as e:
                    errors += 1
                    logger.exception(e)
                    continue
                search_phrases = create_paraphrases(model, [sentence.match]) if paraphrase_search_phrases else [sentence.match]
                if check_result(result, search_phrases, threshold=threshold):
                    success += 1
                    found = True
                    break
            if found:
                break
        count += 1
    table = BeautifulTable()
    table.rows.append(["total sentences", count])
    table.rows.append(["successful matches", success])
    table.rows.append(["non-empty result found", non_empty_count])
    table.rows.append(["query errors", errors])
    print(table)
    logger.info(
        f"{success} successful out of {count}, non-empty result found: {non_empty_count}, query errors: {errors}"
    )


if __name__ == "__main__":
    typer.run(main)
