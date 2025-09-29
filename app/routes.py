import logging
from datetime import datetime

from flask import Blueprint, jsonify, request

from .extensions import db
from .models import Appointment

api = Blueprint("api", __name__)

logger = logging.getLogger(__name__)


@api.route("/appointment", methods=["POST"])
def create_appointment():
    data = request.get_json()
    logger.info("Received data: %s", data)

    if "name" not in data or "phone" not in data:
        return jsonify({"error": "Missing required fields: name, phone"}), 400

    now = datetime.now()
    current_date = now.strftime("%d-%m-%Y")
    current_time = now.strftime("%I:%M:%S %p")

    appointment = Appointment(
        name=data["name"], # type: ignore
        phone_number=data["phone"], # type: ignore
        date=current_date, # type: ignore
        time=current_time, # type: ignore
    )
    db.session.add(appointment)
    db.session.commit()

    logger.info("Appointment created for %s (%s)", data["name"], data["phone"])
    return jsonify({"message": "Your appointment will be confirmed."}), 201


@api.route("/appointments", methods=["GET"])
def get_appointments():
    appointments = Appointment.query.all()
    logger.info("Fetched %d appointments", len(appointments))
    return jsonify([a.to_dict() for a in appointments])
