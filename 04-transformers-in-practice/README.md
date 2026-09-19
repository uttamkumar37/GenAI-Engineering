# 04 — Transformers in Practice

## Fresher

**Concepts**: what tokenization is (BPE at a high level), what a context window is, temperature/top-p/top-k sampling params, what "context length" limits mean practically.

**Resources**:
- [Hugging Face — Tokenizers summary](https://huggingface.co/docs/transformers/tokenizer_summary)
- [Andrej Karpathy — Let's build the GPT Tokenizer (video, first 20 min)](https://www.youtube.com/watch?v=zduSFxRajkE)

**Code** (`code/01-fresher/`):
- `tokenize_playground.py` — use `tiktoken` or HF tokenizer to tokenize sentences, show token counts vs char counts, demonstrate tokenization quirks (numbers, non-English text, whitespace)

**Interview questions**:
- Why does the same sentence sometimes cost more tokens in one language than another? (Tokenizer vocab is trained mostly on English/code corpora — other scripts fragment into more subword tokens.)

## Intermediate

**Concepts**: self-attention mechanism (Q/K/V intuition, not full matrix derivation), multi-head attention, positional encoding, sampling parameters in depth (temperature vs top-p vs top-k interaction), why longer context = more compute (quadratic attention cost).

**Resources**:
- [Jay Alammar — The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)
- [Andrej Karpathy — Let's build GPT from scratch (full video, code along)](https://www.youtube.com/watch?v=kCc8FmEb1nY)

**Code** (`code/02-intermediate/`):
- `attention_from_scratch.py` — scaled dot-product attention with NumPy on toy sequences, visualize attention weights as a heatmap
- `sampling_params_demo.py` — same prompt through mocked logits at different temp/top-p, show output distribution shift

**Interview questions**:
- Explain why attention is O(n²) in sequence length, and why that matters for a 200k-token context window. (Every token attends to every other token — direct cost driver for context-window pricing/latency.)

## Advanced / Senior

**Concepts**: KV cache (why it exists, memory cost per token, how it enables fast autoregressive decoding), why KV cache size determines max concurrent requests on a GPU, grouped-query attention (GQA)/multi-query attention as KV-cache-saving techniques, flash attention (conceptual), how context window limits interact with RAG chunk sizing.

**Resources**:
- Hugging Face — KV cache explainer (search current link/blog, terminology shifts)
- [vLLM blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html)

**Code** (`code/03-advanced/`):
- `kv_cache_manual_sim.py` — simulate decoding with and without KV caching (naive recompute vs cached), measure operation count difference
- `attention_variants_comparison.md` — write-up comparing MHA vs GQA vs MQA memory tradeoffs

**Interview questions**:
- Why does KV cache size, not just model size, limit how many concurrent users a GPU can serve? (Directly connects to Topic 15 vLLM/serving — cache grows with batch size × sequence length × layers.)

## Milestone project (end of Phase 1)

Build and document a small "Transformers Internals Explainer" — a notebook or small app that visualizes tokenization, attention weights, and sampling parameter effects side by side on a real small model (e.g. GPT-2 via HF). Strong portfolio piece since most candidates can't explain internals, only APIs.

## Skip if behind

Flash attention internals and GQA math — keep the conceptual "why it matters for cost/latency" framing only.
