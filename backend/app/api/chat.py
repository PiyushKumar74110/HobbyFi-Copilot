from fastapi import APIRouter, Depends

from app.schemas import (
    ChatRequest,
    ChatResponse,
)

from app.agent.orchestrator import process_query
from app.memory.memory import (
    save_memory,
    get_memory,
)

from app.security.dependencies import get_current_vendor

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    current_vendor=Depends(get_current_vendor),
):

    history = get_memory(
        current_vendor.id
    )

    response = process_query(
        query=request.message,
        vendor_id=current_vendor.id,
        history=history,
    )

    save_memory(
        vendor_id=current_vendor.id,
        user_message=request.message,
        assistant_response=response,
    )

    return ChatResponse(
        response=response
    )