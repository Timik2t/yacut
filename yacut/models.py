from datetime import datetime

from yacut import db
from . constants import SHORT_DB_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(SHORT_DB_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
