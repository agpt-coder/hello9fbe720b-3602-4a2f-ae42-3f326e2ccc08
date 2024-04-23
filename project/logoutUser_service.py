from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class LogoutResponse(BaseModel):
    """
    Response model indicating success of the logout process.
    """

    success: bool
    message: str


async def logoutUser(session_token: str) -> LogoutResponse:
    """
    This endpoint handles user logouts. It requires a valid session token. Upon receiving the request,
    it will invalidate the session token in the database, preventing any further use of it.

    Args:
        session_token (str): The session token provided by the user attempting to logout.

    Returns:
        LogoutResponse: Response model indicating success of the logout process.
    """
    session = await prisma.models.Session.prisma().find_first(
        where={"id": int(session_token), "validUntil": {"gt": datetime.now()}}
    )
    if session is None:
        return LogoutResponse(
            success=False, message="No valid session found or already expired."
        )
    await prisma.models.Session.prisma().update(
        where={"id": session.id}, data={"validUntil": datetime.now()}
    )
    return LogoutResponse(success=True, message="Successfully logged out.")
