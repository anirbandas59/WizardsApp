import logging

from models import db
from datetime import datetime, timedelta, timezone


class ZSession(db.Model):
    __tablename__ = "z_session"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_token = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)
    expires_in = db.Column(db.DateTime, nullable=False)

    def __init__(self, request_token, access_token, login_time):
        self.request_token = request_token
        self.access_token = access_token
        self.login_time = login_time
        self.expires_in = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=6, minute=0, second=0,
                                                                                   microsecond=0)

    def add(self):
        """
        Add a new row to the table z_session or update an existing row
        if the refresh_token is found.
        :return:
        """
        now = self.login_time
        next_day_6am = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        existing_session =  ZSession.query.filter_by(access_token=self.access_token).first()

        if existing_session:
            # Update the existing row
            if existing_session.expires_in > now:
                existing_session.request_token = self.request_token
                existing_session.login_time = self.login_time
                existing_session.expires_in = next_day_6am
        else:
            # Add a new row
            db.session.add(self)

        # Commit the transaction
        db.session.commit()

    @staticmethod
    def invalidate_session(access_token):
        """
        Invalidate the access token row
        :return:
        """
        now = datetime.now()  # Ensure the current time is timezone-aware
        existing_session = db.session.query(ZSession).filter(ZSession.access_token==access_token).first()

        if existing_session:
            if existing_session.expires_in > now:
                existing_session.expires_in = now
                db.session.commit()  # Commit the changes to the database

    def __repr__(self):
        return f"<ZSession {self.id} - Expires In: {self.expires_in}"

    @staticmethod
    def get_access_token(request_token=None):
        now = datetime.now(timezone.utc)
        if request_token:
            session = (
                db.session.query(ZSession)
                .filter(ZSession.expires_in > now)
                .filter(ZSession.request_token == request_token)
                .order_by(ZSession.login_time.desc())
                .first()
            )

        else:
            session = (
                db.session.query(ZSession)
                .filter(ZSession.expires_in > now)
                .order_by(ZSession.login_time.desc())
            )

        return session.access_token if session else None