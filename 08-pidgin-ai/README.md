# 08 · I trained a tiny AI on Nigerian pidgin

A word-level Markov model trained on 93 pidgin sentences I wrote (`corpus.txt`). Version 1 looks at 1 word and Version 2 looks at 2 words.

```bash
python pidgin_ai.py
```

My results: trained in about 1ms. Version 1 said "quick quick quick charge your mouth" 😭. Version 2 sounded fluent, but 48% of its sentences were copied straight from the data.

**Add your own pidgin sentences to `corpus.txt` and retrain it.** The more data, the smarter it gets.
