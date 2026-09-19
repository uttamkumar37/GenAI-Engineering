from __future__ import annotations

# Requires: `pip install vllm` and a CUDA GPU. Written against the vLLM Python API
# (LLM class + SamplingParams) as of vLLM 0.5.x-0.6.x; verify against your installed version.

from dataclasses import dataclass


@dataclass
class VLLMConfig:
    model_name: str = "facebook/opt-125m"
    tensor_parallel_size: int = 1
    gpu_memory_utilization: float = 0.85


def build_vllm_engine(config: VLLMConfig):
    from vllm import LLM  # noqa: F401 (only imported when vllm + GPU are present)

    return LLM(
        model=config.model_name,
        tensor_parallel_size=config.tensor_parallel_size,
        gpu_memory_utilization=config.gpu_memory_utilization,
    )


def generate_batch(engine, prompts: list[str], max_tokens: int = 64) -> list[str]:
    from vllm import SamplingParams

    sampling_params = SamplingParams(temperature=0.0, max_tokens=max_tokens)
    outputs = engine.generate(prompts, sampling_params)
    return [output.outputs[0].text for output in outputs]


if __name__ == "__main__":
    try:
        import vllm  # noqa: F401
    except ImportError:
        print("vllm is not installed in this environment (expected — needs a GPU host).")
        print("On a GPU host: pip install vllm, then run this script to serve a local model.")
        raise SystemExit(0)

    config = VLLMConfig()
    engine = build_vllm_engine(config)
    prompts = [
        "Explain continuous batching in one sentence.",
        "What is PagedAttention?",
    ]
    for prompt, text in zip(prompts, generate_batch(engine, prompts)):
        print(f"PROMPT: {prompt}\nOUTPUT: {text}\n")
