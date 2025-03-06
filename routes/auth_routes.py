from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.auth import *

#auth blueprint
auth_bp = Blueprint("auth_bp", __name__)

#login route
@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()

#register route
@auth_bp.route("/register", methods=["POST"])
def register_route():
    return register()

#refresh route
@auth_bp.route("/refresh", methods=["POST"])
#requir a refresh token so access token can be reset
@jwt_required(refresh=True)
def refresh_route():
    return refresh()

#check session route
@auth_bp.route("/check-session", methods=["GET"])
#require refresh token to reinstate users session
@jwt_required(refresh=True)
def check_session_route():
    return check_session()

#logout route
@auth_bp.route("/logout", methods=["POST"])
def logout_route():
    return logout()