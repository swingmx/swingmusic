from dataclasses import asdict
from flask import jsonify
from flask_jwt_extended import create_access_token, current_user, set_access_cookies
from pydantic import BaseModel, Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from app.db.sqlite.auth import SQLiteAuthMethods as authdb
from app.utils.auth import check_password

bp_tag = Tag(name="Auth", description="Authentication")
api = APIBlueprint("auth", __name__, url_prefix="/auth", abp_tags=[bp_tag])


class LoginBody(BaseModel):
    username: str = Field(description="The username", example="user0")
    password: str = Field(description="The password", example="password0")


@api.post("/login")
def login(body: LoginBody):
    """
    Authenticate using username and password
    """
    res = jsonify({"msg": f"Logged in as {body.username}"})

    user = authdb.get_user_by_username(body.username)

    if user is None:
        return {"msg": "User not found"}, 404

    password_ok = check_password(body.password, user.password)

    if not password_ok:
        return {"msg": "Invalid password"}, 401

    access_token = create_access_token(identity=user.todict())
    set_access_cookies(res, access_token)
    return res


@api.get("/logout")
def logout():
    """
    Log out
    """
    res = jsonify({"msg": "Logged out"})
    res.delete_cookie("access_token_cookie")
    return res


@api.get("/users")
def get_all_users():
    """
    Get all users
    """
    users = authdb.get_all_users()
    return [user.todict_simplified() for user in users]


@api.route("/user")
def get_logged_in_user():
    """
    Get logged in user
    """
    print("current_user", current_user)
    return dict(current_user)
