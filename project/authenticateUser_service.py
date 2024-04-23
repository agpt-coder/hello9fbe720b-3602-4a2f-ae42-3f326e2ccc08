from datetime import datetime, timedelta

import prisma
import prisma.enums
import prisma.models
from passlib.context import CryptContext
from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    """
    Response model containing the user's basic information along with a session token after a successful login.
    """

    session_token: str
    user_id: int
    user_email: str
    user_role: prisma.enums.Role


async def authenticateUser(username: str, password: str) -> UserLoginResponse:
    """
    This endpoint allows users to log in by submitting their credentials. It validates the username and password against the database,
    and if successful, generates a new session token which is returned along with the user's basic information.

    Args:
        username (str): The username the user uses to login.
        password (str): The password associated with the username for user authentication. It's expected to be hashed server-side for verification.

    Returns:
        UserLoginResponse: Response model containing the user's basic information along with a session token after a successful login.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user and pwd_context.verify(password, user.password):
        session_token = pwd_context.hash(str(datetime.now()))
        new_session = await prisma.models.Session.prisma().create(
            data={
                "userId": user.id,
                "createdAt": datetime.now(),
                "validUntil": datetime.now() + timedelta(days=1),
            }
        )
        return UserLoginResponse(
            session_token=session_token,
            user_id=user.id,
            user_email=user.email,
            user_role=user.role,
        )
    else:
        raise ValueError("Invalid username or password")
