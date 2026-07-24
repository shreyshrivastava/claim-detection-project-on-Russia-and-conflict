"""Embedding helpers extracted from the historical notebooks.

The public demo does not import torch or transformers at startup. These helpers
are lazy and optional so CI remains CPU-only and free of model downloads.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


def get_device() -> Any:
    """Choose the best available torch device when torch is installed."""

    try:
        import torch
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError("torch is required for BERT embeddings but is not installed") from exc

    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def bert_cls_embeddings(
    texts: Sequence[str],
    *,
    tokenizer: Any,
    bert_model: Any,
    batch_size: int = 32,
    max_length: int = 512,
    device: Any | None = None,
) -> np.ndarray:
    """Return BERT `[CLS]` embeddings for texts using caller-provided objects.

    This mirrors the notebook logic, but keeps loading decisions outside the
    function so tests and deployments do not accidentally download models.
    """

    try:
        import torch
    except ImportError as exc:  # pragma: no cover - optional dependency path
        raise RuntimeError("torch is required for BERT embeddings but is not installed") from exc

    if not texts:
        return np.empty((0, 0))

    resolved_device = device or get_device()
    bert_model = bert_model.to(resolved_device)
    bert_model.eval()

    batches: list[np.ndarray] = []
    for start in range(0, len(texts), batch_size):
        batch = list(texts[start : start + batch_size])
        encoded = tokenizer(
            batch,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=max_length,
        )
        encoded = {key: value.to(resolved_device) for key, value in encoded.items()}
        with torch.no_grad():
            output = bert_model(**encoded)
        batches.append(output.last_hidden_state[:, 0, :].cpu().numpy())

    return np.vstack(batches)
