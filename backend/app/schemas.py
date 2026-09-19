from pydantic import BaseModel


from datetime import datetime





class ChatRequest(BaseModel):


    message: str


    





class ChatResponse(BaseModel):


    response: str





class ApprovalResponse(BaseModel):


    id: str


    status: str