from database import db
from datetime import datetime

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
    in_diet = db.Column(db.Boolean(), nullable=False)
