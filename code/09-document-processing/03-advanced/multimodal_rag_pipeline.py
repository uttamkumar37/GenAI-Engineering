# requires ANTHROPIC_API_KEY for AnthropicMultimodalLLM; FakeMultimodalLLM needs nothing.
# image captioning uses a deterministic fake captioner by default (swap in a real vision call for production).
from __future__ import annotations

import base64
import hashlib
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")
EMBEDDING_DIM = 16
SAMPLE_IMAGE = Path(__file__).parent.parent / "02-intermediate" / "sample_data" / "scanned_page.png"

TEXT_DOCS = [
    "Acme Corp ships all domestic orders via standard ground carrier within 2 business days.",
    "International orders may incur customs delays of up to 10 business days.",
]


@dataclass
class RagItem:
    item_id: str
    kind: str  # "text" | "image"
    text_for_retrieval: str  # raw text, or an image caption used as its retrieval surrogate
    payload: str  # the text itself, or an image path


def fake_embed(text: str) -> list[float]:
    return [
        (hashlib.sha256(f"{text}:{i}".encode()).digest()[0] / 255.0) * 2 - 1
        for i in range(EMBEDDING_DIM)
    ]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


class Captioner(ABC):
    @abstractmethod
    def caption(self, image_path: Path) -> str: ...


class AnthropicCaptioner(Captioner):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def caption(self, image_path: Path) -> str:
        image_data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/png", "data": image_data},
                        },
                        {"type": "text", "text": "Briefly describe what this document image contains."},
                    ],
                }
            ],
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeCaptioner(Captioner):
    # deterministic stand-in: a fixed caption describing the known sample scanned image
    def caption(self, image_path: Path) -> str:
        return "A shipping notice document showing an order number, ship date, and shipped item contents."


def build_index(captioner: Captioner, image_paths: list[Path]) -> list[RagItem]:
    items = [RagItem(f"text-{i}", "text", doc, doc) for i, doc in enumerate(TEXT_DOCS)]
    for i, path in enumerate(image_paths):
        caption = captioner.caption(path)
        items.append(RagItem(f"image-{i}", "image", caption, str(path)))
    return items


def retrieve(items: list[RagItem], query: str, top_k: int = 2) -> list[RagItem]:
    query_vec = fake_embed(query)
    scored = [(cosine_similarity(query_vec, fake_embed(item.text_for_retrieval)), item) for item in items]
    scored.sort(key=lambda t: t[0], reverse=True)
    return [item for _, item in scored[:top_k]]


class MultimodalLLM(ABC):
    @abstractmethod
    def answer(self, query: str, items: list[RagItem]) -> str: ...


class AnthropicMultimodalLLM(MultimodalLLM):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def answer(self, query: str, items: list[RagItem]) -> str:
        content: list[dict] = []
        for item in items:
            if item.kind == "text":
                content.append({"type": "text", "text": f"Text context: {item.payload}"})
            else:
                image_data = base64.standard_b64encode(Path(item.payload).read_bytes()).decode("utf-8")
                content.append(
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}}
                )
        content.append({"type": "text", "text": query})
        response = self.client.messages.create(
            model=self.model, max_tokens=300, messages=[{"role": "user", "content": content}]
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeMultimodalLLM(MultimodalLLM):
    # deterministic stand-in: summarizes retrieved text and image captions without real reasoning
    def answer(self, query: str, items: list[RagItem]) -> str:
        parts = []
        for item in items:
            if item.kind == "text":
                parts.append(f"[text:{item.item_id}] {item.payload}")
            else:
                parts.append(f"[image:{item.item_id} caption] {item.text_for_retrieval}")
        return f"Answering '{query}' using: " + " | ".join(parts)


def multimodal_rag(captioner: Captioner, llm: MultimodalLLM, query: str, image_paths: list[Path]) -> str:
    items = build_index(captioner, image_paths)
    retrieved = retrieve(items, query)
    return llm.answer(query, retrieved)


if __name__ == "__main__":
    if not SAMPLE_IMAGE.exists():
        import sys

        sys.path.insert(0, str(SAMPLE_IMAGE.parent.parent))
        from ocr_scanned_doc import make_synthetic_scan

        make_synthetic_scan(SAMPLE_IMAGE)

    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    captioner: Captioner = AnthropicCaptioner() if has_key else FakeCaptioner()
    llm: MultimodalLLM = AnthropicMultimodalLLM() if has_key else FakeMultimodalLLM()

    result = multimodal_rag(captioner, llm, "What was shipped and what's the shipping notice about?", [SAMPLE_IMAGE])
    print(result)
