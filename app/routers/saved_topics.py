# favorites.py (или saved_topics.py)
from uuid import UUID
from fastapi import APIRouter
from app.dependencies.services import SavedTopicServiceDep

router = APIRouter(prefix="/topics", tags=["Favorites"])

@router.post("/{topic_id}/favorite")
async def add_to_favorites(service: SavedTopicServiceDep):
    ...

@router.delete("/{topic_id}/favorite")
async def remove_from_favorites(service: SavedTopicServiceDep):
    ...