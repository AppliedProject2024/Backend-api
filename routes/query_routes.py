from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.query import *


query_bp = Blueprint("query_bp", __name__)

#route to Q&A queries
@query_bp.route("/query", methods=["POST"])
@jwt_required()
def query_route():
    return query()

#route to handle summary queries
@query_bp.route("/summary", methods=["POST"])
@jwt_required()
def summary_route():
    return summary()

#route to handle mcq queries
@query_bp.route("/mcq", methods=["POST"])
@jwt_required()
def mcq_route():
    return mcq()