from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.feedback import *

#feedback blueprint
feedback_bp = Blueprint("feedback_bp", __name__)

#submit feedback route
@feedback_bp.route("/submit", methods=["POST"])
@jwt_required()
def Submit_feedback_route():
    return submit_feedback()

#get feedback route
@feedback_bp.route("/get", methods=["GET"])
@jwt_required()
def get_feedback_route():
    feedback_data = get_feedback()
    return feedback_data

