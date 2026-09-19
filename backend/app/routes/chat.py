from fastapi import APIRouter

from app.schemas import (
    ChatRequest,
    ChatResponse,
)

from app.agent.orchestrator import (
    process_query,
)

from app.memory.memory import (
    save_memory,
    get_memory,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):

    # -------------------------
    # Load Memory
    # -------------------------

    history = get_memory(
        request.vendor_id
    )


    # -------------------------
    # Process Query
    # -------------------------

    response = process_query(
        query=request.message,
        vendor_id=request.vendor_id,
        history=history,
    )


    # -------------------------
    # Save Memory
    # -------------------------

    save_memory(
        vendor_id=request.vendor_id,
        user_message=request.message,
        assistant_response=response,
    )


    # -------------------------
    # Return Response
    # -------------------------

    return ChatResponse(
        response=response
    )