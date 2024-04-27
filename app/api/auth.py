import json
from dataclasses import asdict
from functools import wraps
from flask import jsonify
from flask_jwt_extended import create_access_token, current_user, set_access_cookies
from pydantic import BaseModel, Field
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint

from app.db.sqlite.auth import SQLiteAuthMethods as authdb
from app.utils.auth import check_password, encode_password

bp_tag = Tag(name="Auth", description="Authentication stuff")
api = APIBlueprint("auth", __name__, url_prefix="/auth", abp_tags=[bp_tag])


def admin_required():
    """
    Decorator to require admin role
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "admin" not in current_user["roles"]:
                return {"msg": "Only admins can do that!"}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


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


class UpdateProfileBody(BaseModel):
    email: str = Field("", description="The email")
    username: str = Field("", description="The username", example="user0")
    password: str = Field("", description="The password", example="password0")
    roles: list[str] = Field([], description="The roles")


@api.put("/profile/update")
def update_profile(body: UpdateProfileBody):
    user = {
        "id": current_user["id"],
        "email": body.email,
        "username": body.username,
        "password": body.password,
        "roles": body.roles,
    }

    # only admins can update roles
    if body.roles:
        if "admin" in current_user["roles"]:
            # prevent admin from locking themselves out
            roles = set(body.roles)
            roles.add("admin")
            user["roles"] = json.dumps(list(roles))
        else:
            user.pop("roles")

    if user["password"]:
        user["password"] = encode_password(user["password"])

    # remove empty values
    clean_user = {k: v for k, v in user.items() if v}
    return authdb.update_user(clean_user)


@api.post("/profile/create")
@admin_required()
def create_user(body: UpdateProfileBody):
    if not body.username or not body.password:
        return {"msg": "Username and password are required"}, 400

    user = {
        "username": body.username,
        "password": encode_password(body.password),
        "roles": json.dumps([]),
    }

    # check if user already exists
    if authdb.get_user_by_username(user["username"]):
        return {"msg": "Username already exists"}, 400

    userid = authdb.insert_user(user)
    return authdb.get_user_by_id(userid).todict()


@api.post("/profile/guest/create")
@admin_required()
def create_guest_user():
    """
    Create a guest user
    """
    # check if guest user already exists
    guest_user = authdb.get_user_by_username("guest")

    if guest_user:
        return {
            "msg": "Guest user already exists",
        }, 400

    userid = authdb.insert_guest_user()

    if userid:
        return {
            "msg": "Guest user created",
        }

    return {
        "msg": "Failed to create guest user",
    }, 500


class DeleteUseBody(BaseModel):
    username: str = Field("", description="The username")


@api.delete("/profile/delete")
@admin_required()
def delete_user(body: DeleteUseBody):
    """
    Delete a user by username
    """
    # prevent admin from deleting themselves
    if body.username == current_user["usrname"]:
        return {"msg": "Sorry! you cannot delete yourselfu"}, 400

    # prevent deleting the only admin
    users = authdb.get_all_users()
    admins = [user for user in users if "admin" in user.roles]
    if len(admins) == 1 and admins[0].username == body.username:
        return {"msg": "Cannot delete the only admin"}, 400

    authdb.delete_user_by_username(body.username)
    return {"msg": f"User {body.username} deleted"}


@api.get("/logout")
def logout():
    """
    Log out
    """
    res = jsonify({"msg": "Logged out"})
    res.delete_cookie("access_token_cookie")
    return res


class GetAllUsersQuery(BaseModel):
    simplified: bool = Field(
        False, description="Whether to return simplified user data"
    )


@api.get("/users")
def get_all_users(query: GetAllUsersQuery):
    """
    Get all users
    """
    users = authdb.get_all_users()

    # remove guest user
    users = [user for user in users if user.username != "guest"]

    # reverse list to show latest users first
    users = list(reversed(users))

    # bring admins to the front
    users = sorted(users, key=lambda x: "admin" in x.roles, reverse=True)

    if query.simplified:
        return [user.todict_simplified() for user in users]

    return [user.todict() for user in users]


@api.route("/user")
def get_logged_in_user():
    """
    Get logged in user
    """
    return dict(current_user)
