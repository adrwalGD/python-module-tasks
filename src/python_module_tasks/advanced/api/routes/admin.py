from fastapi import APIRouter, HTTPException, Depends, Header

router = APIRouter()
ADMIN_TOKEN = "hardcoded_admin_token"


def admin_auth(token: str = Header()):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@router.get("/admin-action", dependencies=[Depends(admin_auth)])
async def perform_admin_action():
    """Perform an admin action (dummy)"""
    return {"message": "Admin action successful"}
