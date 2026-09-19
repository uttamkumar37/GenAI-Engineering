# 04 — Transformers in Practice — Intermediate

**Concepts**: self-attention mechanism (Q/K/V intuition, not full matrix derivation), multi-head attention, positional encoding, sampling parameters in depth (temperature vs top-p vs top-k interaction), why longer context = more compute (quadratic attention cost).

**Resources**:
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [Andrej Karpathy — Let's build GPT from scratch (full video, code along)](https://www.youtube.com/watch?v=kCc8FmEb1nY)

**Code** (`code/04-transformers-in-practice/02-intermediate/`):
- `attention_from_scratch.py` — scaled dot-product attention with NumPy on toy sequences, visualize attention weights as a heatmap
- `sampling_params_demo.py` — same prompt through mocked logits at different temp/top-p, show output distribution shift

**Interview questions**:
- Explain why attention is O(n²) in sequence length, and why that matters for a 200k-token context window. (Every token attends to every other token — direct cost driver for context-window pricing/latency.)
