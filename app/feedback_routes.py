from flask import Blueprint, request, jsonify
from config.sqlite_config import db_connect
from flask_jwt_extended import jwt_required, get_jwt_identity

#feedback blueprint
feedback_bp = Blueprint("feedback_bp", __name__)

#submit feedback route
@feedback_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_feedback():
    #get user email from JWT
    user_email = get_jwt_identity()
    data = request.json
    #get feedback data from request
    feedback_type, feedback = data["feedback_type"], data["feedback"]

    #check if feedback type and feedback are provided
    if not feedback_type and not feedback:
        return jsonify({"error": "Feedback type and feedback required"}), 400
    
    #connect to sqlite database
    connect = db_connect()
    #insert the feedback into the database
    connect.execute(
        "INSERT INTO feedback (user_email, feedback_type, feedback) VALUES (?, ?, ?)",
        (user_email, feedback_type, feedback)
    )
    #commit changes and close connection
    connect.commit()
    connect.close()

    #return success message
    return jsonify({"message": "Feedback submitted"}), 200

#get feedback route
@feedback_bp.route("/get", methods=["GET"])
@jwt_required()
def get_feedback():
    #connect to sqlite database
    connect = db_connect()
    #get all feedback from the database
    feedback = connect.execute("SELECT * FROM feedback").fetchall()
    #close connection
    connect.close()

    #return feedback list
    feedback_list = [{"id": row["id"], "user_email": row["user_email"], "feedback_type": row["feedback_type"], "feedback": row["feedback"], "created_at": row["created_at"]} for row in feedback]
    return jsonify(feedback_list), 200

