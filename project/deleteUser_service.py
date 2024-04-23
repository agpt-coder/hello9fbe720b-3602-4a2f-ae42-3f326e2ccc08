from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model for the delete user endpoint. Confirms that the operation was successful and provides any necessary messages or errors.
    """

    message: str
    success: bool


async def deleteUser(session_token: str) -> DeleteUserResponse:
    """
    This endpoint allows users to delete their account. It requires a valid session token, and upon successful validation, it deletes the user from the database and invalidates any active sessions.

    Args:
        session_token (str): A valid session token used to authenticate the request to delete a user account.

    Returns:
        DeleteUserResponse: Response model for the delete user endpoint. Confirms that the operation was successful and provides any necessary messages or errors.
    """
    session = await prisma.models.Session.prisma().find_first(
        where={"id": session_token, "validUntil": {"gt": datetime.now()}}
    )
    if session:
        user_id = session.userId
        await prisma.models.User.prisma().delete(where={"id": user_id})
        return DeleteUserResponse(
            message="prisma.models.User and sessions successfully deleted.",
            success=True,
        )
    else:
        return DeleteUserResponse(
            message="Invalid session token or session expired.", success=False
        )
