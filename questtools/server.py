"""Utilities to run the QuestTools web server."""

from __future__ import annotations

import threading
import time
import webbrowser
from pathlib import Path
from .repository import QuestRepository
from .web import create_app


def run_server(
    data_path: Path | str,
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    open_browser: bool = False,
) -> None:
    """Start the QuestTools FastAPI server."""

    app_path = Path(data_path)
    repository = QuestRepository(app_path)
    app = create_app(repository, data_path=app_path.resolve())

    if open_browser:
        url = f"http://{host}:{port}/"

        def _open() -> None:
            time.sleep(1.0)
            webbrowser.open(url)

        threading.Thread(target=_open, daemon=True).start()

    try:
        import uvicorn
    except ImportError as exc:  # pragma: no cover - runtime guard
        raise RuntimeError("uvicorn is required to run the server") from exc

    uvicorn.run(app, host=host, port=port)
