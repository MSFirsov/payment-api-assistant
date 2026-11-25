from pathlib import Path

from payment_api_assistant.chunking import chunk_markdown


def test_chunk_markdown_keeps_source_and_id(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text("# Платежи\n\n## Комиссии\n\nТекст правила.\n", encoding="utf-8")

    chunk, = chunk_markdown(path)

    assert chunk.text == "Текст правила."
    assert chunk.document == "example.md"
    assert chunk.section_path == ("Платежи", "Комиссии")
    assert chunk.id == "example.md#1"
    assert chunk_markdown(path)[0].id == chunk.id


def test_chunk_markdown_splits_long_section_at_paragraphs(tmp_path: Path) -> None:
    path = tmp_path / "example.md"
    path.write_text("# Платежи\n\n## Комиссии\n\nПервый абзац.\n\nВторой абзац.\n", encoding="utf-8")

    chunks = chunk_markdown(path, chunk_size=16)

    assert [chunk.text for chunk in chunks] == ["Первый абзац.", "Второй абзац."]
    assert [chunk.section_path for chunk in chunks] == [("Платежи", "Комиссии"), ("Платежи", "Комиссии")]
    assert [chunk.id for chunk in chunks] == ["example.md#1", "example.md#2"]
