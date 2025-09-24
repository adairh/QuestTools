"""FastAPI application for the QuestTools management UI."""

from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ..repository import QuestRepository
from . import schemas


def create_app(repository: QuestRepository, *, data_path: Path | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(title="QuestTools UI")

    templates_dir = Path(__file__).parent / "templates"
    static_dir = Path(__file__).parent / "static"
    templates = Jinja2Templates(directory=str(templates_dir))
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    def get_repository() -> QuestRepository:
        return repository

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> HTMLResponse:  # pragma: no cover - template rendering
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "data_path": str(data_path) if data_path else None,
            },
        )

    @app.get("/api/document", response_model=schemas.DocumentResponse)
    def get_document(repo: QuestRepository = Depends(get_repository)) -> schemas.DocumentResponse:
        document = repo.get_document()
        quests = [schemas.QuestResponse(**quest.to_dict()) for quest in document.quests]
        return schemas.DocumentResponse(title=document.title, overview=document.overview, quests=quests)

    @app.put("/api/document", response_model=schemas.DocumentResponse)
    def update_document(
        payload: schemas.DocumentUpdate,
        repo: QuestRepository = Depends(get_repository),
    ) -> schemas.DocumentResponse:
        document = repo.update_document(title=payload.title, overview=payload.overview)
        quests = [schemas.QuestResponse(**quest.to_dict()) for quest in document.quests]
        return schemas.DocumentResponse(title=document.title, overview=document.overview, quests=quests)

    @app.post("/api/quests", response_model=schemas.QuestResponse, status_code=201)
    def create_quest(
        payload: schemas.QuestCreate,
        repo: QuestRepository = Depends(get_repository),
    ) -> schemas.QuestResponse:
        quest = repo.create_quest(payload.model_dump())
        return schemas.QuestResponse(**quest.to_dict())

    @app.put("/api/quests/{quest_id}", response_model=schemas.QuestResponse)
    def update_quest(
        quest_id: int,
        payload: schemas.QuestUpdate,
        repo: QuestRepository = Depends(get_repository),
    ) -> schemas.QuestResponse:
        try:
            quest = repo.update_quest(quest_id, payload.model_dump(exclude_unset=True))
        except KeyError as exc:  # pragma: no cover - defensive
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return schemas.QuestResponse(**quest.to_dict())

    @app.delete("/api/quests/{quest_id}", status_code=204)
    def delete_quest(quest_id: int, repo: QuestRepository = Depends(get_repository)) -> None:
        try:
            repo.delete_quest(quest_id)
        except KeyError as exc:  # pragma: no cover - defensive
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    return app
