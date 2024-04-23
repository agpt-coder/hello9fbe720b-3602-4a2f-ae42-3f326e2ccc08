import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserRegistrationResponse(BaseModel):
    """
    Includes confirmation of user creation and their unique identifier.
    """

    message: str
    userId: int


async def registerUser(
    username: str, email: str, password: str
) -> UserRegistrationResponse:
    """
    This endpoint allows new users to register. It expects a user object with fields like username, password, and email.
    This route will validate the provided data, create a new user in the database, and return a success message along with
    the user ID.

    Args:
        username (str): Unique username chosen by the user.
        email (str): User's email address which acts as a unique identifier for login and communication.
        password (str): Password for securing the user's account, which will be hashed before stored in the database.

    Returns:
        UserRegistrationResponse: Includes confirmation of user creation and their unique identifier.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "password": hashed_password,
            "role": prisma.enums.Role.Guest,
        }
    )
    response = UserRegistrationResponse(
        message="User successfully registered.", userId=user.id
    )
    return response
