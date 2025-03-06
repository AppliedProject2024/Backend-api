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