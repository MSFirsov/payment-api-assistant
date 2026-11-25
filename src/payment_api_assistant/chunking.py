from dataclasses import dataclass
from pathlib import Path

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter


@dataclass(frozen=True)
class Chunk:
    """Хранит текст фрагмента и сведения о его источнике.

    Attributes:
        id: Идентификатор фрагмента в пределах каталога документов.
        text: Текст фрагмента.
        document: Имя исходного Markdown-файла.
        section_path: Заголовки от верхнего уровня до текущего раздела.
    """

    id: str
    text: str
    document: str
    section_path: tuple[str, ...]


def chunk_markdown(path: Path, *, chunk_size: int = 600) -> list[Chunk]:
    """Читает Markdown-файл и возвращает фрагменты с путями разделов.

    Args:
        path: Путь к Markdown-файлу в UTF-8.
        chunk_size: Максимальная длина фрагмента в символах.

    Returns:
        Фрагменты в порядке появления в документе.

    Raises:
        OSError: Файл не удалось прочитать.
        ValueError: Размер фрагмента меньше единицы.
    """
    headers = [(str("#" * level), f"h{level}") for level in range(1, 7)]
    markdown = path.read_text(encoding="utf-8")
    sections = MarkdownHeaderTextSplitter(headers).split_text(markdown)
    chunks: list[Chunk] = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)

    for section in sections:
        section_path = tuple(
            section.metadata[key] for _, key in headers if key in section.metadata
        )
        text = section.page_content.replace("  \n", "\n\n")
        for part in splitter.split_text(text):
            chunks.append(
                Chunk(
                    id = f"{path.name}#{len(chunks) + 1}",
                    text=part,
                    document=path.name,
                    section_path=section_path,
                )
            )
    return chunks
