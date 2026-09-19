# MHA vs GQA vs MQA: KV Cache Memory Tradeoffs

## The core idea

KV cache memory per token scales with `num_kv_heads × head_dim × num_layers × 2 (K and V) × bytes_per_element`.
Multi-Head Attention (MHA), Grouped-Query Attention (GQA), and Multi-Query Attention (MQA) differ only in
how many *key/value* heads they keep, while the number of *query* heads stays the same (one per attention head).

## Multi-Head Attention (MHA)

Every query head has its own dedicated key/value head. If a model has `H` heads, it stores `H` sets of K/V
per layer per token.

- KV cache size: `H × head_dim × num_layers × 2 × seq_len` per sequence.
- Quality: best — each head learns fully independent K/V projections.
- Cost: largest KV cache, directly limits max batch size / concurrent requests on a fixed-memory GPU.

## Multi-Query Attention (MQA)

All query heads share a single key/value head.

- KV cache size: `1 × head_dim × num_layers × 2 × seq_len` per sequence — an `H`x reduction vs MHA.
- Quality: some loss vs MHA, since all heads are forced to attend using the same K/V representation.
- Cost: dramatically smaller cache, so many more concurrent sequences fit in the same GPU memory; also less
  memory bandwidth per decode step, which speeds up autoregressive generation (memory-bound at batch size 1).

## Grouped-Query Attention (GQA)

A middle ground: query heads are split into `G` groups, and each group shares one key/value head
(`1 < G < H`). This is what most modern production LLMs (Llama 2/3, Mistral) actually use.

- KV cache size: `G × head_dim × num_layers × 2 × seq_len` per sequence.
- Quality: much closer to MHA than MQA, because groups still specialize somewhat.
- Cost: tunable tradeoff — pick `G` to balance quality against how much KV cache memory you can afford.

## Why this matters for serving

- KV cache memory (not model weight size) is usually the binding constraint on how many concurrent
  requests/users a single GPU can serve, because it grows linearly with `batch_size × seq_len`, while model
  weights are fixed.
- Reducing KV heads (MQA/GQA) is one of the main levers — alongside quantization and techniques like
  PagedAttention (vLLM) — for increasing achievable concurrency without adding GPUs.
- Flash Attention (conceptually) doesn't change *what* is cached, just makes computing attention over the
  cache faster and more memory-efficient by fusing the softmax + matmul steps and avoiding materializing the
  full attention matrix — it's complementary to GQA/MQA, not a replacement for the KV-cache-size problem.

## Rule of thumb

| Variant | KV heads | Relative cache size | Relative quality |
|---|---|---|---|
| MHA | `H` (all heads) | 1x (baseline) | highest |
| GQA | `G` (grouped, e.g. `H/8`) | `G/H` | close to MHA |
| MQA | `1` | `1/H` | lowest, but often acceptable |

Choosing among them is a quality-vs-throughput decision made at model-architecture time (it isn't something
you can switch at serving time without retraining), which is why it matters to know before picking a model
for a latency/concurrency-sensitive deployment.
