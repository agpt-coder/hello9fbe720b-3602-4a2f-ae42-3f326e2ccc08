from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserDetailsResponseModel(BaseModel):
    """
    This model structures the user information returned from the UserDetails endpoint. It should include all necessary details that a client might require to proceed with session-related tasks or displays.
    """

    username: str
    email: str
    role: prisma.enums.Role


async def getUserDetails(session_token: str) -> UserDetailsResponseModel:
    """
    This endpoint retrieves detailed information of a logged-in user. It requires a valid session token and returns user information such as username, email, and role.

    Args:
        session_token (str): The session token provided by the user as part of the authentication process. It should be included in the header for security reasons.

    Returns:
        UserDetailsResponseModel: This model structures the user information returned from the UserDetails endpoint. It should include all necessary details that a client might require to proceed with session-related tasks or displays.

    Example:
        session_token = 'some-valid-token'
        user_details = await getUserDetails(session_token)
        print(user_details.username, user_details.email, user_details.role)
    """
    session = await prisma.models.Session.prisma().find_first(
        where={"id": session_token, "validUntil": {"gte": datetime.now()}},
        include={"user": True},
    )
    if session and session.user:
        user = session.user
        return UserDetailsResponseModel(
            username=user.email.split("@")[0], email=user.email, role=user.role.name
        )
    else:
        raise ValueError("Invalid session token or session expired.")
