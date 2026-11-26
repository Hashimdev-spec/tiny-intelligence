# 02 · I trained an AI to read handwriting

A small neural network (scikit-learn `MLPClassifier`) trained on 1,797 handwritten digits (8×8 pixels each). Then I test it on digits I drew myself, including a Nigerian-style 1 with a base.

```bash
python digits_ai.py
```

My results: trained in about 0.5s, 96.67% accuracy, and it read my Nigerian 1 as a **2** (71% sure).

Try it yourself: edit the `mine` strokes in the script to draw your own digits.
