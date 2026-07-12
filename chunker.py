from dataclasses import dataclass

@dataclass(frozen=True)
class ChunkingConfig:
    chunk_size: int = 700
    chunk_overlap: int = 120

def chunk_text(text: str, config: ChunkingConfig | None = None) -> list[str]:
    cfg = config or ChunkingConfig()
    if cfg.chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if cfg.chunk_overlap < 0 or cfg.chunk_overlap >= cfg.chunk_size:
        raise ValueError("invalid chunk_overlap")

    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + cfg.chunk_size, len(text))
        if end < len(text):
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - cfg.chunk_overlap
    return chunks
