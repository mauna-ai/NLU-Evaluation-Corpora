import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer


class Model:
    def __init__(self, model_name):
        self._model_name = model_name
        self._torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        self._tokenizer = PegasusTokenizer.from_pretrained(model_name)

    def prepare(self):
        self.model = PegasusForConditionalGeneration.from_pretrained(
            self._model_name
        ).to(self._torch_device)

    def run(self, input_text, num_return_sequences):
        batch = self._tokenizer.prepare_seq2seq_batch(
            [input_text],
            truncation=True,
            padding="longest",
            max_length=60,
            return_tensors="pt",
        ).to(self._torch_device)
        translated = self.model.generate(
            **batch,
            max_length=60,
            num_beams=10,
            num_return_sequences=num_return_sequences,
            temperature=1.5
        )
        tgt_text = self._tokenizer.batch_decode(translated, skip_special_tokens=True)
        return tgt_text
