import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.authenticateUser_service
import project.deleteUser_service
import project.getUserDetails_service
import project.getWelcomeMessage_service
import project.logoutUser_service
import project.registerUser_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="hello", lifespan=lifespan, description="create a single hello world app"
)


@app.post(
    "/users/register",
    response_model=project.registerUser_service.UserRegistrationResponse,
)
async def api_post_registerUser(
    username: str, email: str, password: str
) -> project.registerUser_service.UserRegistrationResponse | Response:
    """
    This endpoint allows new users to register. It expects a user object with fields like username, password, and email. This route will validate the provided data, create a new user in the database, and return a success message along with the user ID.
    """
    try:
        res = await project.registerUser_service.registerUser(username, email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/welcome-message",
    response_model=project.getWelcomeMessage_service.WelcomeMessageResponse,
)
async def api_get_getWelcomeMessage(
    user_id: Optional[int],
) -> project.getWelcomeMessage_service.WelcomeMessageResponse | Response:
    """
    This route fetches a personalized 'Hello World' message. It retrieves user data using the User Management's API to personalize the greeting if the user is logged in, or defaults to a generic greeting for guests. The expected response is a JSON object containing the personalized or default greeting message. This route utilizes the User Management API for fetching user data if available.
    """
    try:
        res = await project.getWelcomeMessage_service.getWelcomeMessage(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/delete", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    session_token: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    This endpoint allows users to delete their account. It requires a valid session token, and upon successful validation, it deletes the user from the database and invalidates any active sessions.
    """
    try:
        res = await project.deleteUser_service.deleteUser(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put("/users/update", response_model=project.updateUser_service.UserUpdateResponse)
async def api_put_updateUser(
    session_token: str, email: Optional[str], password: Optional[str]
) -> project.updateUser_service.UserUpdateResponse | Response:
    """
    This route enables users to update their profile information. It requires fields they are updating like email or password, and a valid session token. The request is validated, and upon success, the user's data in the database is updated.
    """
    try:
        res = await project.updateUser_service.updateUser(
            session_token, email, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users/logout", response_model=project.logoutUser_service.LogoutResponse)
async def api_post_logoutUser(
    session_token: str,
) -> project.logoutUser_service.LogoutResponse | Response:
    """
    This endpoint handles user logouts. It requires a valid session token. Upon receiving the request, it will invalidate the session token in the database, preventing any further use of it.
    """
    try:
        res = await project.logoutUser_service.logoutUser(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/users/login", response_model=project.authenticateUser_service.UserLoginResponse
)
async def api_post_authenticateUser(
    username: str, password: str
) -> project.authenticateUser_service.UserLoginResponse | Response:
    """
    This endpoint allows users to log in by submitting their credentials. It validates the username and password against the database, and if successful, generates a new session token which is returned along with the user's basic information.
    """
    try:
        res = await project.authenticateUser_service.authenticateUser(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/details",
    response_model=project.getUserDetails_service.UserDetailsResponseModel,
)
async def api_get_getUserDetails(
    session_token: str,
) -> project.getUserDetails_service.UserDetailsResponseModel | Response:
    """
    This endpoint retrieves detailed information of a logged-in user. It requires a valid session token and returns user information such as username, email, and role.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(session_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
