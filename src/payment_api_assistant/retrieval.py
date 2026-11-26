from langchain_core.vectorstores import VectorStore

from payment_api_assistant.chunking import Chunk


def retrieve(question: str, k: int = 4, *, store: VectorStore) -> list[Chunk]:
    """Находит фрагменты документации, подходящие под вопрос.

    Args:
        question: Вопрос пользователя.
        k: Максимальное число фрагментов в результате.
        store: Готовый векторный индекс с текстами и их источниками.

    Returns:
        Фрагменты по убыванию сходства с вопросом.

    Raises:
        ValueError: Вопрос пуст, k меньше единицы или у результата отсутствует ID.
    """
    question = question.strip()
    if not question:
        raise ValueError("Введите вопрос.")
    if k < 1:
        raise ValueError("k должно быть положительным.")

    documents = store.similarity_search(question, k=k)
    chunks: list[Chunk] = []
    for document in documents:
        if not document.id:
            raise ValueError("У найденного фрагмента отсутствует ID.")
        chunks.append(
            Chunk(
                id=document.id,
                text=document.page_content,
                document=document.metadata["document"],
                section_path=tuple(document.metadata["section_path"]),
            )
        )
    return chunks
