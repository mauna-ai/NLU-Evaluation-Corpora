# Holmes extraxctor benchmarking script

## Requirements
 - Python 3.7 (not likely to work with more recent versions, like 3.8 or 3.9)

## Installation
 - Create a virtual environment
```
$ virtualenv -p $(which python3.7) venv 
```

 - Install dependencies
 ```
 $ source venv/bin/activate
 (venv37) $ pip install -r requirements.txt
 ```
 This could take a while, because it downloads spacy models

 ## Usage
 In order to see the help message run the following command:
 ```
 (venv37) $ python main.py --help
 ```
 The output should be as follows:
 ```
 Usage: main.py [OPTIONS]

Options:
  --paraphrase / --no-paraphrase  [default: True]
  --large-model / --no-large-model
                                  [default: False]
  --sentences INTEGER             [default: 0]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
 ```
 --paraphrase / --no-paraphrase - Enable/disable paraphrasing, enabled by default

 --large-model / --no-large-model - Use `en_core_web_lg` spacy model if enabled, disabled by default

 --sentences INTEGER - Restrict the amount of sentences to test, this could be useful for quick checks, as checking all sentences takes several hours

 To run the program with default parameters, just execute:
 ```
 (venv37) $ python main.py
 ```
 The above code will run with paraphrasing enables and with `en_core_web_md` model. This could take a cioouple of hours to finish.

 In order to tweak something, see command line options descriptions above.

 ## Logging and results
 The program writes logs and results to `holmes_extractor.log`.

 Logs could look as follows:
 ```
 [2021-01-27 16:10:45,064] - ------------------------------------------------------------------------------------------------------------------------
[2021-01-27 16:10:45,084] - Using en_core_web_md model
[2021-01-27 16:11:01,630] - Non-empty result found: [{'search_phrase': 'Somebody requires insurance', 'document': '', 'index_within_document': 1, 'sentences_within_document': 'I require insurance', 'negated': False, 'uncertain': False, 'involves_coreference': False, 'overall_similarity_measure': '1.0', 'word_matches': [{'search_phrase_word': 'require', 'document_word': 'require', 'document_phrase': 'require', 'match_type': 'direct', 'similarity_measure': '1.0', 'involves_coreference': False, 'extracted_word': 'require', 'explanation': 'Matches REQUIRE directly.'}, {'search_phrase_word': 'insurance', 'document_word': 'insurance', 'document_phrase': 'insurance', 'match_type': 'direct', 'similarity_measure': '1.0', 'involves_coreference': False, 'extracted_word': 'insurance', 'explanation': 'Matches INSURANCE directly.'}]}]
[2021-01-27 16:11:14,142] - 0 successful out of 1, query errors: 0
[2021-01-27 16:13:58,998] - ------------------------------------------------------------------------------------------------------------------------
[2021-01-27 16:13:58,999] - Using en_core_web_md model
[2021-01-27 16:14:15,313] - Non-empty result found: [{'search_phrase': 'Somebody requires insurance', 'document': '', 'index_within_document': 1, 'sentences_within_document': 'I require insurance', 'negated': False, 'uncertain': False, 'involves_coreference': False, 'overall_similarity_measure': '1.0', 'word_matches': [{'search_phrase_word': 'require', 'document_word': 'require', 'document_phrase': 'require', 'match_type': 'direct', 'similarity_measure': '1.0', 'involves_coreference': False, 'extracted_word': 'require', 'explanation': 'Matches REQUIRE directly.'}, {'search_phrase_word': 'insurance', 'document_word': 'insurance', 'document_phrase': 'insurance', 'match_type': 'direct', 'similarity_measure': '1.0', 'involves_coreference': False, 'extracted_word': 'insurance', 'explanation': 'Matches INSURANCE directly.'}]}]
[2021-01-27 16:14:28,763] - 0 successful out of 1, non-empty result found: 1, query errors: 0
[2021-01-27 16:16:10,412] - ------------------------------------------------------------------------------------------------------------------------
[2021-01-27 16:16:10,435] - Using en_core_web_md model
[2021-01-27 16:16:24,544] - Non-empty result found: [{'document': '',
  'index_within_document': 1,
  'involves_coreference': False,
  'negated': False,
  'overall_similarity_measure': '1.0',
  'search_phrase': 'Somebody requires insurance',
  'sentences_within_document': 'I require insurance',
  'uncertain': False,
  'word_matches': [{'document_phrase': 'require',
                    'document_word': 'require',
                    'explanation': 'Matches REQUIRE directly.',
                    'extracted_word': 'require',
                    'involves_coreference': False,
                    'match_type': 'direct',
                    'search_phrase_word': 'require',
                    'similarity_measure': '1.0'},
                   {'document_phrase': 'insurance',
                    'document_word': 'insurance',
                    'explanation': 'Matches INSURANCE directly.',
                    'extracted_word': 'insurance',
                    'involves_coreference': False,
                    'match_type': 'direct',
                    'search_phrase_word': 'insurance',
                    'similarity_measure': '1.0'}]}]
[2021-01-27 16:16:40,577] - 0 successful out of 1, non-empty result found: 1, query errors: 0
 ```

 The most important lines are the ones that look like this:
 ```
 ... 0 successful out of 1, non-empty result found: 1, query errors: 0
 ```
 This means that 1 test was performed with 0 successful matches, but one non-empty result (after parsing by Holmes extractor) was found (it just wasn't equal to the right sentence).

 The number of successful matches is the value that must be improved.

 ## Warning!!!

 It might be that the script incorrectly gives a low number of successful matches (not because of how holmes extractor works) as a result.
 
 In this case, one needs to check the amount of non-empty result found. If this number is high (or at least gigher than the number of matches), then the script needs to be debugged.
