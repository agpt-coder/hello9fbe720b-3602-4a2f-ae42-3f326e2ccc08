from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class WelcomeMessageResponse(BaseModel):
    """
    Response model for returning a personalized or default 'Hello World' message.
    """

    message: str


async def getWelcomeMessage(user_id: Optional[int]) -> WelcomeMessageResponse:
    """
    This route fetches a personalized 'Hello World' message. It retrieves user data using the User Management's API to personalize the greeting if the user is logged in, or defaults to a generic greeting for guests. The expected response is a JSON object containing the personalized or default greeting message. This route utilizes the User Management API for fetching user data if available.

    Args:
    user_id (Optional[int]): Optional user ID to personalize the greeting, assumed to be fetched from session or token validation.

    Returns:
    WelcomeMessageResponse: Response model for returning a personalized or default 'Hello World' message.
    """
    if user_id is not None:
        user = await prisma.models.User.prisma().find_unique(
            where={"id": user_id}, include={"sessions": True}
        )
        if user and any((s.validUntil > datetime.now() for s in user.sessions)):
            message_content = f"Hello {user.email}!"
        else:
            message_content = "Hello World!"
    else:
        message_content = "Hello World!"
    return WelcomeMessageResponse(message=message_content)
