# 02 — Math & ML Essentials — Intermediate

**Concepts**: gradient descent (batch/stochastic/mini-batch), loss functions (MSE, cross-entropy), softmax, overfitting/regularization, train/val/test splits, basic linear algebra for NN layers (matrix multiply as a linear transform).

**Resources**:
- [3Blue1Brown — Neural Networks series, episodes 1-2](https://www.3blue1brown.com/topics/neural-networks)
- [StatQuest — Cross Entropy](https://www.youtube.com/watch?v=6ArSys5qHAU)

**Code** (`code/02-math-ml-essentials/02-intermediate/`):
- `gradient_descent_variants.py` — batch vs SGD vs mini-batch on same dataset, compare convergence
- `softmax_crossentropy.py` — from scratch, compare to `torch.nn.functional` output

**Interview questions**:
- Why is cross-entropy loss preferred over MSE for classification, especially next-token prediction? (Penalizes confident wrong predictions harder; matches probabilistic interpretation of softmax outputs.)
