import io

from fastapi import APIRouter, Response

from backend.models.event_model import EventModel
from backend.services.event_generator import create_ics_file


router = APIRouter()

@router.post("/events/")
def create_event(event: EventModel):
    ics_content = create_ics_file(event)
    ics_file = io.BytesIO(ics_content.encode("utf-8"))

    return Response(
        content=ics_file.getvalue(),
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=eventos.ics"}
    )
