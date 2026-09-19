# 02 — Math & ML Essentials

## Fresher

**Concepts**: vectors/matrices, dot product, mean/variance, basic probability (conditional, Bayes intuition), pandas basics (DataFrame, groupby, merge).

**Resources**:
- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [pandas — 10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Khan Academy — Bayes theorem](https://www.khanacademy.org/math/statistics-probability/probability-library/conditional-probability-independence/a/conditional-probability-and-independence)

**Code** (`code/01-fresher/`):
- `vector_ops.py` — dot product, norm, cosine similarity from scratch
- `pandas_basics.py` — load CSV, groupby, filter

**Interview questions**:
- Why do embeddings use high-dimensional vectors instead of a single similarity score? (Direction encodes multiple semantic axes simultaneously.)

## Intermediate

**Concepts**: gradient descent (batch/stochastic/mini-batch), loss functions (MSE, cross-entropy), softmax, overfitting/regularization, train/val/test splits, basic linear algebra for NN layers (matrix multiply as a linear transform).

**Resources**:
- [3Blue1Brown — Neural Networks series, episodes 1-2](https://www.3blue1brown.com/topics/neural-networks)
- [StatQuest — Cross Entropy](https://www.youtube.com/watch?v=6ArSys5qHAU)

**Code** (`code/02-intermediate/`):
- `gradient_descent_variants.py` — batch vs SGD vs mini-batch on same dataset, compare convergence
- `softmax_crossentropy.py` — from scratch, compare to `torch.nn.functional` output

**Interview questions**:
- Why is cross-entropy loss preferred over MSE for classification, especially next-token prediction? (Penalizes confident wrong predictions harder; matches probabilistic interpretation of softmax outputs.)

## Advanced / Senior

**Concepts**: why LLM training uses AdamW not vanilla SGD, learning rate schedules (warmup + cosine decay), gradient clipping, numerical stability (log-sum-exp trick), why loss curves plateau/spike during pretraining and what that signals.

**Resources**:
- Sebastian Raschka — "Understanding AdamW" (search current link; blog moves)
- [Andrej Karpathy — Let's build GPT (video, math sections)](https://www.youtube.com/watch?v=kCc8FmEb1nY)

**Code** (`code/03-advanced/`):
- `adamw_from_scratch.py`
- `lr_schedule_visualizer.py` — plot warmup+cosine decay curve
- `numerical_stability_demo.py` — naive softmax overflow vs log-sum-exp trick

**Interview questions**:
- A training loss spikes suddenly at step 50k — what are your top 3 hypotheses? (LR too high / bad batch (data issue) / gradient explosion — ties to clipping.)

## Skip if behind

Advanced-level math derivations; keep the intuition-level videos, drop hand-deriving AdamW.
