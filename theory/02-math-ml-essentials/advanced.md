# 02 — Math & ML Essentials — Advanced / Senior

**Concepts**: why LLM training uses AdamW not vanilla SGD, learning rate schedules (warmup + cosine decay), gradient clipping, numerical stability (log-sum-exp trick), why loss curves plateau/spike during pretraining and what that signals.

**Resources**:
- Sebastian Raschka — "Understanding AdamW" (search current link; blog moves)
- [Andrej Karpathy — Let's build GPT (video, math sections)](https://www.youtube.com/watch?v=kCc8FmEb1nY)

**Code** (`code/02-math-ml-essentials/03-advanced/`):
- `adamw_from_scratch.py`
- `lr_schedule_visualizer.py` — plot warmup+cosine decay curve
- `numerical_stability_demo.py` — naive softmax overflow vs log-sum-exp trick

**Interview questions**:
- A training loss spikes suddenly at step 50k — what are your top 3 hypotheses? (LR too high / bad batch (data issue) / gradient explosion — ties to clipping.)
