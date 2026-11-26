"""Dayo Tries #2 - I trained a tiny AI to read handwriting... then tried to fool it."""
import numpy as np, time, json
from PIL import Image, ImageDraw, ImageFont
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

digits = load_digits()                      # 1,797 handwritten digits, 8x8 pixels each
X, y = digits.data, digits.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=4)
net = MLPClassifier(hidden_layer_sizes=(64,), max_iter=600, random_state=1)
t = time.perf_counter(); net.fit(Xtr, ytr); train_s = time.perf_counter() - t
acc = net.score(Xte, yte)
print(f"dataset {len(X)} images, train {len(Xtr)}, test {len(Xte)}; trained in {train_s:.2f}s; accuracy {acc*100:.2f}%")

def draw(strokes, w=10):
    """my own 'handwriting': strokes in a 64x64 box, shrunk to 8x8 like the dataset (0..16)"""
    im = Image.new("L", (64, 64), 0); d = ImageDraw.Draw(im)
    for s in strokes:
        if s[0] == "line": d.line(s[1], fill=255, width=w, joint="curve")
        elif s[0] == "arc": d.arc(s[1], s[2], s[3], fill=255, width=w)
        elif s[0] == "ell": d.ellipse(s[1], outline=255, width=w)
    small = np.asarray(im.resize((8, 8), Image.BILINEAR), dtype=float) / 255 * 16
    return small.reshape(-1), np.asarray(im)

mine = {
 "5": [("line", [(46, 8), (20, 8), (18, 30)]), ("arc", (10, 24, 50, 58), 270, 135)],
 "4": [("line", [(38, 6), (12, 40), (52, 40)]), ("line", [(40, 20), (40, 60)])],
 "7": [("line", [(12, 10), (52, 10), (26, 58)])],
 "0": [("ell", (14, 6, 50, 58))],
 "1 (with a base)": [("line", [(22, 16), (34, 6), (34, 56)]), ("line", [(20, 56), (48, 56)])],
 "9": [("ell", (16, 6, 48, 32)), ("line", [(46, 18), (44, 58)])],
 "3": [("arc", (16, 4, 48, 32), 200, 90), ("arc", (14, 28, 50, 60), 270, 160)],
 "2": [("arc", (14, 4, 50, 36), 190, 20), ("line", [(48, 24), (14, 56), (52, 56)])],
}
res = {}
for name, strokes in mine.items():
    v, big = draw(strokes)
    p = net.predict_proba([v])[0]
    res[name] = dict(pred=int(np.argmax(p)), conf=float(p.max()), img=big.tolist(), small=v.reshape(8, 8).tolist())
    print(f"I drew {name:16s} -> AI says {np.argmax(p)} ({p.max()*100:.2f}%)")
# a couple of test-set examples with confidence
ex = {}
for want in (5, 8):
    i = int(np.where(yte == want)[0][0]); p = net.predict_proba([Xte[i]])[0]
    ex[want] = dict(pred=int(np.argmax(p)), conf=float(p.max()), small=Xte[i].reshape(8, 8).tolist())
    print(f"test {want}: AI says {np.argmax(p)} ({p.max()*100:.4f}%)")
json.dump(dict(acc=acc, n=len(X), ntr=len(Xtr), nte=len(Xte), train_s=train_s, mine=res, ex=ex), open("results.json", "w"))
