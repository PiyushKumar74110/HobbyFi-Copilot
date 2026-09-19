from fastapi import APIRouter, HTTPException


from app.services.approval_service import (
    approve_request,
    reject_request,
    get_approval_request
)


router = APIRouter(

    prefix="/approval",

    tags=["Approval"]

)



@router.get("/{approval_id}")
def get_request(
    approval_id: int
):


    request = get_approval_request(
        approval_id
    )


    if not request:

        raise HTTPException(

            status_code=404,

            detail="Approval request not found"

        )


    return request





@router.post("/{approval_id}/approve")
def approve(
    approval_id: int
):


    result = approve_request(
        approval_id
    )


    return {

        "status":
        "approved",

        "data":
        result

    }





@router.post("/{approval_id}/reject")
def reject(
    approval_id: int
):


    result = reject_request(
        approval_id
    )


    return {

        "status":
        "rejected",

        "data":
        result

    }