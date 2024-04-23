from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserUpdateResponse(BaseModel):
    """
    Defines the structure of the response after updating the user's information. It confirms the completion of the update process.
    """

    success: bool
    message: str


async def updateUser(
    session_token: str, email: Optional[str], password: Optional[str]
) -> UserUpdateResponse:
    """
    This route enables users to update their profile information. It requires fields they are updating like email or password, and a valid session token. The request is validated, and upon success, the user's data in the database is updated.

    Args:
        session_token (str): The session token of the user to verify their identity and session validity.
        email (Optional[str]): The new email address to update, if changing.
        password (Optional[str]): The new password to update, if changing.

    Returns:
        UserUpdateResponse: Defines the structure of the response after updating the user's information. It confirms the completion of the update process.
    """
    session = await prisma.models.Session.prisma().find_first(
        where={"id": int(session_token), "validUntil": {"gt": datetime.now()}},
        include={"user": True},
    )
    if not session:
        return UserUpdateResponse(
            success=False, message="Invalid or expired session token."
        )
    user = session.user
    update_data = {}
    if email:
        update_data["email"] = email
    if password:
        update_data["password"] = password
    if not update_data:
        return UserUpdateResponse(success=False, message="No updates to perform.")
    updated_user = await prisma.models.User.prisma().update(
        where={"id": user.id}, data=update_data
    )
    if updated_user:
        return UserUpdateResponse(success=True, message="User updated successfully.")
    else:
        return UserUpdateResponse(success=False, message="Failed to update user.")
