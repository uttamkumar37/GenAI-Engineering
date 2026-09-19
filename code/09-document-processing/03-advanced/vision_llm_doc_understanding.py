# requires ANTHROPIC_API_KEY for AnthropicVisionClient; FakeVisionClient needs nothing.
# requires pytesseract + tesseract binary + pillow for the OCR+text comparison path.
from __future__ import annotations

import base64
import os
import sys
from abc import ABC, abstractmethod
from pathlib import Path

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-5")

DOC_IMAGE_PATH = Path(__file__).parent.parent / "02-intermediate" / "sample_data" / "scanned_page.png"
QUESTION = "What is the order number and what items were shipped?"


class VisionClient(ABC):
    @abstractmethod
    def answer_from_image(self, image_path: Path, question: str) -> str: ...


class AnthropicVisionClient(VisionClient):
    def __init__(self, model: str = MODEL) -> None:
        import anthropic

        self.model = model
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def answer_from_image(self, image_path: Path, question: str) -> str:
        image_data = base64.standard_b64encode(image_path.read_bytes()).decode("utf-8")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/png", "data": image_data},
                        },
                        {"type": "text", "text": question},
                    ],
                }
            ],
        )
        return next(b.text for b in response.content if b.type == "text")


class FakeVisionClient(VisionClient):
    # deterministic stand-in: "reads" the image by using the ground-truth text it was rendered from
    def answer_from_image(self, image_path: Path, question: str) -> str:
        from ocr_scanned_doc import SCANNED_TEXT  # the exact text the sample image was rendered from

        ground_truth = "\n".join(SCANNED_TEXT)
        return f"[vision-LLM, simulated] Reading the document layout directly:\n{ground_truth}"


def ocr_then_text_llm(image_path: Path, question: str) -> str:
    sys.path.insert(0, str(image_path.parent.parent))
    from ocr_scanned_doc import run_ocr

    ocr_text = run_ocr(image_path)
    return f"[OCR+text pipeline] extracted text:\n{ocr_text}\n(answer would be derived from this noisy text)"


if __name__ == "__main__":
    sys.path.insert(0, str(DOC_IMAGE_PATH.parent.parent))
    if not DOC_IMAGE_PATH.exists():
        from ocr_scanned_doc import make_synthetic_scan

        make_synthetic_scan(DOC_IMAGE_PATH)

    vision_client: VisionClient = (
        AnthropicVisionClient() if os.environ.get("ANTHROPIC_API_KEY") else FakeVisionClient()
    )

    print("=== Vision-LLM direct approach ===")
    print(vision_client.answer_from_image(DOC_IMAGE_PATH, QUESTION))

    print("\n=== OCR + text pipeline approach ===")
    print(ocr_then_text_llm(DOC_IMAGE_PATH, QUESTION))
