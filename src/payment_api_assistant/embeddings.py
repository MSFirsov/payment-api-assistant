from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

from payment_api_assistant.chunking import Chunk
from payment_api_assistant.config import Settings


def create_embeddings(settings: Settings) -> OpenAIEmbeddings:
    """Создаёт клиент эмбеддингов для OpenAI-совместимого API LM Studio.

    Args:
        settings: Адрес API, ключ и идентификатор модели.

    Returns:
        Клиент, который отправляет текст модели эмбеддингов.
    """
    return OpenAIEmbeddings(
        base_url=settings.base_url,
        api_key=settings.api_key,
        model=settings.embedding_model,
        check_embedding_ctx_length=False,
        model_kwargs={"encoding_format": "float"},
    )


def build_vector_store(chunks: list[Chunk], embeddings: Embeddings) -> InMemoryVectorStore:
    """Создаёт индекс в памяти и добавляет в него фрагменты.

    Args:
        chunks: Фрагменты Markdown с идентификаторами и путями разделов.
        embeddings: Клиент, который вычисляет векторы для текстов фрагментов.

    Returns:
        Индекс с векторами, текстами и метаданными источников.
    """
    documents = [
        Document(
            id=chunk.id,
            page_content=chunk.text,
            metadata={
                "document": chunk.document,
                "section_path": list(chunk.section_path),
            }
        )
        for chunk in chunks
    ]

    store = InMemoryVectorStore(embedding=embeddings)
    if documents:
        store.add_documents(documents)
    return store
