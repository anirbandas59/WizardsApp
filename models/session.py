import logging

from models import db
from datetime import datetime, timedelta, timezone


class ZSession(db.Model):
    __tablename__ = "z_session"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    request_token = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)
    expires_in = db.Column(db.DateTime, nullable=False)

    def __init__(self, request_token, access_token, login_time):
        self.request_token = request_token
        self.access_token = access_token
        self.login_time = login_time
        self.expires_in = datetime.now(timezone.utc) + timedelta(hours=3)

    def add(self):
        """
        Add a new row to the table z_session or update an existing row
        if the refresh_token is found.
        :return:
        """
        db.session.add(self)
        db.session.commit()

        # Check for existing session
        # try:
        #     existing_session = db.session.query.filter(request_token=self.request_token).first()
        #
        #     if existing_session:
        #         existing_session.access_token = self.access_token
        #         existing_session.login_time = self.login_time
        #         existing_session.expires_in = self.expires_in
        #     else:
        #         db.session.add(self)
        #
        #     db.session.commit()
        # except Exception as e:
        #     logging.log(e)


    def __repr__(self):
        return f"<ZSession {self.id} - Expires In: {self.expires_in}"


    def get_access_token(self, request_token):
        now = datetime.now(timezone.utc)
        session = (
            db.session.query
            .filter(self.expires_in > now)
            .filter(self.request_token == request_token)
            .order_by(self.login_time.desc())
            .first()
        )
        return session.access_token if session else None
