from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expenses(db.Model):
    id = db.Column(
        db.String,
        unique=True,
        nullable=False,
        primary_key=True
    )
    note = db.Column(
        db.String,
        nullable=False
    )
    amount = db.Column(
        db.Float,
        nullable=False
    )
    timestamp = db.Column(
        db.Float,
        nullable=False
    )