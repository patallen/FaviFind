from favifind import db


class Favicon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), nullable=False, unique=True)
    favicon = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=db.func.now())
