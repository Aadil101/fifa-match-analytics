import os.path
import urllib.parse

from fastapi import APIRouter, HTTPException

from app import ocr
from app.api.deps import CurrentUser, SessionDep
from app.models import Message

router = APIRouter(prefix="/ocr", tags=["ocr"])

# TODO: Make route authenticated
@router.post("/{image_type}/{image_path}")
def perform_ocr(
    *,
    image_path: str,
    image_type: str, # TODO: make image_type an enum
) -> Message:
    image_path_decoded = urllib.parse.unquote(image_path)
    if not os.path.isfile(image_path_decoded):
        raise HTTPException(status_code=400, detail="Image path is not a file on disk")
    # TODO: Validate image_type
    # TODO: Consider running OCR asynchronously
    ocr.perform_ocr(image_path=image_path, image_type=image_type)
    return Message(message="Completed OCR")
