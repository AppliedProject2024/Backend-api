from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.query import *


query_bp = Blueprint("query_bp", __name__)

#route to handle pdf uploads
@query_bp.route("/query", methods=["POST"])
@jwt_required()
def query_route():
    return query()