from formula1_app.database import db


class Chart(db.Model):
    __tablename__ = "charts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    identifier = db.Column(db.String(50), unique=True, nullable=False)
    filename = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
