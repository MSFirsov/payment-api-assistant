# payment-api-assistant

Проект помощника по документации вымышленного платёжного API.

Проект нарезает `docs/payments.md` по заголовкам и делит длинные разделы по абзацам. Каждый фрагмент хранит текст, имя файла, путь раздела и ID. LM Studio вычисляет эмбеддинги фрагментов, а `InMemoryVectorStore` хранит векторы вместе с текстами и метаданными источников. Поиск по вопросу выводит подходящие фрагменты, их разделы и имена файлов.

## Запуск

Из корня проекта с Python 3.14 и `uv` выполни:

```bash
uv sync --locked
uv run payment-api-assistant
uv run pytest -q
```

## Поиск по документации

Запусти локальный сервер LM Studio и загрузи модель эмбеддингов. Скопируй `.env.example` в `.env`, если его ещё нет, и сверь `EMBEDDING_MODEL` с идентификатором загруженной модели.

```bash
uv run payment-api-assistant search "Какая комиссия за платёж картой?" --k 1
```

Команда выведет один фрагмент из раздела «Платежи → Комиссии» файла `payments.md`.

## Сборка индекса

```bash
uv run python - <<'PY'
from pathlib import Path

from payment_api_assistant.chunking import chunk_markdown
from payment_api_assistant.config import load_settings
from payment_api_assistant.embeddings import build_vector_store, create_embeddings

chunks = chunk_markdown(Path("docs/payments.md"))
store = build_vector_store(chunks, create_embeddings(load_settings()))
print(f"Записей в индексе: {len(store.store)}")
PY
```

Для `payments.md` команда выведет `Записей в индексе: 2`.
