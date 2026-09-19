from __future__ import annotations

from dataclasses import dataclass


@dataclass
class QuantizationProfile:
    precision: str
    relative_vram_gb: float
    tokens_per_second: float
    quality_score: float  # 0-1, proxy for downstream eval accuracy (e.g. RAGAS faithfulness)


# Hardcoded synthetic figures representative of published fp16/int8/int4 tradeoffs for a ~7B model.
# Real numbers require `pip install bitsandbytes` (or AWQ/GPTQ) + a GPU; see load_real_model() below.
BENCHMARK_PROFILES: list[QuantizationProfile] = [
    QuantizationProfile("fp16", relative_vram_gb=14.0, tokens_per_second=42.0, quality_score=0.93),
    QuantizationProfile("int8", relative_vram_gb=7.5, tokens_per_second=58.0, quality_score=0.91),
    QuantizationProfile("int4", relative_vram_gb=4.0, tokens_per_second=71.0, quality_score=0.84),
]


def load_real_model(precision: str):
    # Requires: transformers, accelerate, bitsandbytes, and a CUDA GPU.
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig

    quant_config = None
    if precision == "int8":
        quant_config = BitsAndBytesConfig(load_in_8bit=True)
    elif precision == "int4":
        quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="float16")

    return AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-2-7b-hf",
        quantization_config=quant_config,
        torch_dtype="auto" if precision == "fp16" else None,
    )


def compare_profiles(profiles: list[QuantizationProfile]) -> None:
    baseline = next(p for p in profiles if p.precision == "fp16")
    print(f"{'precision':10s} {'VRAM(GB)':>10s} {'tok/s':>8s} {'quality':>8s} {'speedup':>9s} {'quality_drop':>13s}")
    for p in profiles:
        speedup = p.tokens_per_second / baseline.tokens_per_second
        quality_drop = baseline.quality_score - p.quality_score
        print(
            f"{p.precision:10s} {p.relative_vram_gb:10.1f} {p.tokens_per_second:8.1f} "
            f"{p.quality_score:8.2f} {speedup:8.2f}x {quality_drop:13.3f}"
        )


if __name__ == "__main__":
    compare_profiles(BENCHMARK_PROFILES)
    print(
        "\nNote: these are synthetic/reference numbers so the comparison logic is demonstrable "
        "without a GPU. Swap in load_real_model() outputs when running on real hardware."
    )
