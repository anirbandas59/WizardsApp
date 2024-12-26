import os

from dotenv import load_dotenv

load_dotenv()

class DBSettings:

    def __init__(self):
        db_username = os.getenv('DB_USERNAME')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_name = os.getenv('DB_NAME')
        self.database_uri = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

    def get_db_uri(self):
       return self.database_uri


DATABASE_URI = DBSettings().get_db_uri()