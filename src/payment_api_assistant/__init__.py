from pathlib import Path

from payment_api_assistant.chunking import chunk_markdown


def main() -> None:
    """Выводит фрагменты документа и их источники в терминал.

    Raises:
        OSError: Учебный Markdown-файл не удалось прочитать.
    """
    for chunk in chunk_markdown(Path("docs/payments.md")):
        section = " -> ".join(chunk.section_path)
        print(f"Раздел: {section}")
        print(f"Файл: {chunk.document}")
        print(chunk.text)
        print()
