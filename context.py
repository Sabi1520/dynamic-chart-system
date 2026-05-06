from fastapi import APIRouter
from mcp.mcp_store import mcp

router = APIRouter()

@router.get("/context")
def get_context():
    return mcp.get_context()

@router.post("/context")
def update_context(payload: dict):
    return mcp.update_context(payload)
