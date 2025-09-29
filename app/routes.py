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

    # Validate required fields
    required_fields = ["name", "phone", "appointment_date", "appointment_time"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify(
            {"error": f"Missing required fields: {', '.join(missing_fields)}"}
        ), 400

    now = datetime.now()
    current_date = now.strftime(format="%d-%m-%Y")
    current_time = now.strftime(format="%I:%M:%S %p")

    appointment = Appointment(
        name=data["name"],
        phone_number=data["phone"],
        created_date=current_date,
        created_time=current_time,
        appointment_date=data["appointment_date"],
        appointment_time=data["appointment_time"],
    )
    db.session.add(instance=appointment)
    db.session.commit()

    logger.info(
        "Appointment created for %s (%s) on %s at %s",
        data["name"],
        data["phone"],
        data["appointment_date"],
        data["appointment_time"],
    )
    return jsonify({"message": "Your appointment will be confirmed."}), 201


@api.route("/appointments", methods=["GET"])
def get_appointments():
    date = request.args.get("date")
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")

    query = Appointment.query

    if date:
        query = query.filter(Appointment.appointment_date == date)
    elif from_date and to_date:
        query = query.filter(
            Appointment.appointment_date >= from_date,
            Appointment.appointment_date <= to_date,
        )
    elif from_date or to_date:
        return jsonify(
            {"error": "Both from_date and to_date are required for range filtering"}
        ), 400

    appointments = query.all()
    logger.info("Fetched %d appointments", len(appointments))
    return jsonify([a.to_dict() for a in appointments])
