# 04 — Transformers in Practice — Advanced / Senior

**Concepts**: KV cache (why it exists, memory cost per token, how it enables fast autoregressive decoding), why KV cache size determines max concurrent requests on a GPU, grouped-query attention (GQA)/multi-query attention as KV-cache-saving techniques, flash attention (conceptual), how context window limits interact with RAG chunk sizing.

**Resources**:
- Hugging Face — KV cache explainer (search current link/blog, terminology shifts)
- [vLLM blog — PagedAttention](https://blog.vllm.ai/2023/06/20/vllm.html)

**Code** (`code/04-transformers-in-practice/03-advanced/`):
- `kv_cache_manual_sim.py` — simulate decoding with and without KV caching (naive recompute vs cached), measure operation count difference
- `attention_variants_comparison.md` — write-up comparing MHA vs GQA vs MQA memory tradeoffs

**Interview questions**:
- Why does KV cache size, not just model size, limit how many concurrent users a GPU can serve? (Directly connects to Topic 15 vLLM/serving — cache grows with batch size × sequence length × layers.)
