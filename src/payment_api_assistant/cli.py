from argparse import ArgumentParser
from pathlib import Path

from payment_api_assistant.chunking import chunk_markdown
from payment_api_assistant.config import load_settings
from payment_api_assistant.embeddings import build_vector_store, create_embeddings
from payment_api_assistant.retrieval import retrieve


def main() -> None:
    """Выводит фрагменты документа и их источники в терминал.

    Raises:
        OSError: Учебный Markdown-файл не удалось прочитать.
    """
    parser = ArgumentParser(description="Поиск по документации платёжного API")
    subparsers = parser.add_subparsers(dest="command")
    search_parser = subparsers.add_parser("search", help="Найти фрагменты по вопросу")
    search_parser.add_argument("question", help="Вопрос к документации")
    search_parser.add_argument("--k", type=int, default=4, help="Максимум фрагментов")
    args = parser.parse_args()

    if args.command == "search":
        if not args.question.strip():
            search_parser.error("Введите вопрос.")
        if args.k < 1:
            search_parser.error("--k должно быть положительным.")

    chunks = chunk_markdown(Path("docs/payments.md"))

    if args.command == "search":
        store = build_vector_store(chunks, create_embeddings(load_settings()))
        chunks = retrieve(args.question, k=args.k, store=store)
        if not chunks:
            print("Фрагменты не найдены.")
            return

    for chunk in chunks:
        section = " -> ".join(chunk.section_path)
        print(f"Раздел: {section}")
        print(f"Файл: {chunk.document}")
        print(chunk.text)
        print()
