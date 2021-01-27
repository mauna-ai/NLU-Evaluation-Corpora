import spacy
import neuralcoref
from holmes_extractor import semantics


class PatchedEnglishSemanticAnalyzer(semantics.EnglishSemanticAnalyzer):
    def __init__(self, *, model, perform_coreference_resolution, debug):
        self.nlp = spacy.load(model)
        if perform_coreference_resolution == None and self.model_supports_coreference_resolution():
            perform_coreference_resolution = True
        if perform_coreference_resolution and not self.nlp.has_pipe("neuralcoref"):
            neuralcoref.add_to_pipe(self.nlp)
        self.model = model
        self.perform_coreference_resolution = perform_coreference_resolution
        self.debug = debug
        self._derivational_dictionary = self._load_derivational_dictionary()
