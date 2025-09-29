from .extensions import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    appointment_date = db.Column(db.String(20))
    appointment_time = db.Column(db.String(20))
    created_date = db.Column(db.String(20))
    created_time = db.Column(db.String(20))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "created_date": self.created_date,
            "created_time": self.created_time,
            "appointment_date": self.appointment_date,
            "appointment_time": self.appointment_time,
        }
