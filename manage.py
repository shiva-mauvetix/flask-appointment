from app import create_app
from app.extensions import db
from app.models import Appointment

app = create_app()


# For flask db commands (migrations)
@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Appointment": Appointment}
