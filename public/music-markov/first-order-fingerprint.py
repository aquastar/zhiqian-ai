"""
First-order Markov fingerprint of musical style.

One monophonic piece -> one 12x12 row-stochastic transition matrix over scale
degrees (pitch classes relative to the piece's tonic) -> 144 features.
No hand-designed musical features, no tuning. A plain multinomial logistic
regression then has to name the style of a piece it has never seen.

Reported result: 70.9% five-fold accuracy over 1,000 pieces in six traditions
(majority-class baseline 20%).

Corpora: Bach chorales, Palestrina, Monteverdi, 14th-century Italian song
(Trecento), the Essen Folksong Collection, and Ryan's Mammoth Collection of
fiddle tunes -- all public symbolic sets, parsed with music21 into
seqs_v2.json as {style: [{"tonic": int, "mel": [[pitch, onset, dur], ...]}]},
with pitch == -1 for a rest.

Written with AI assistance and checked by hand; if you build on it, re-verify.
Computation used the Rochester Institute of Technology Research Computing
cluster, DOI 10.34788/0S3G-QD15.
"""
import json, numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix

REST, V = -1, 12
D = json.load(open("seqs_v2.json"))
styles = sorted(D)

X, y = [], []
for s in styles:
    for pc in D[s]:
        q = [(p - pc["tonic"]) % 12 for p, onset, dur in pc["mel"] if p != REST]
        if len(q) < 24:
            continue
        M = np.zeros((V, V))
        for a, b in zip(q, q[1:]):
            M[a, b] += 1
        r = M.sum(1, keepdims=True)
        X.append((M / np.where(r == 0, 1, r)).ravel())   # row-stochastic, 144 numbers
        y.append(s)
X, y = np.array(X), np.array(y)

cv = StratifiedKFold(5, shuffle=True, random_state=0)
clf = LogisticRegression(max_iter=4000)
print("%d pieces, %d features" % X.shape)
print("5-fold accuracy: %.1f%%" % (100 * cross_val_score(clf, X, y, cv=cv).mean()))

C = confusion_matrix(y, cross_val_predict(clf, X, y, cv=cv), labels=styles)
print("\n%-16s" % "true\\pred" + "".join("%12s" % s[:11] for s in styles))
for i, s in enumerate(styles):
    print("%-16s" % s[:15] + "".join("%11.0f%%" % (100 * v / C[i].sum()) for v in C[i]))
