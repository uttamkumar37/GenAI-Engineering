# 04 — Transformers in Practice — Fresher

**Concepts**: what tokenization is (BPE at a high level), what a context window is, temperature/top-p/top-k sampling params, what "context length" limits mean practically.

**Resources**:
- [Hugging Face — Tokenizers summary](https://huggingface.co/docs/transformers/tokenizer_summary)
- [Andrej Karpathy — Let's build the GPT Tokenizer (video, first 20 min)](https://www.youtube.com/watch?v=zduSFxRajkE)

**Code** (`code/04-transformers-in-practice/01-fresher/`):
- `tokenize_playground.py` — use `tiktoken` or HF tokenizer to tokenize sentences, show token counts vs char counts, demonstrate tokenization quirks (numbers, non-English text, whitespace)

**Interview questions**:
- Why does the same sentence sometimes cost more tokens in one language than another? (Tokenizer vocab is trained mostly on English/code corpora — other scripts fragment into more subword tokens.)
