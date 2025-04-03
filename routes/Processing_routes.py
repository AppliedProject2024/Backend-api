from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.processing import *

#feedback blueprint
file_bp = Blueprint("file_bp", __name__)

#route to handle pdf uploads
@file_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_route():
    return upload_pdf()

#route to get user document filenames
@file_bp.route("/extract", methods=["GET"])
@jwt_required()
def extract_route():
    return get_user_documents()

#route to delete user document filenames
@file_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_route():
    return delete_document()