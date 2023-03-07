import os

# Environment == The computer your app is running on
# with os.getenv we provide a variable name to look for on the computer
# if the variable is not found/undefined, set the second string as the value
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'abc123')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'postgresql://ryan_live:123456@localhost:3000/mydb')  # change to db in postgres uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'burntheboats'
    DEBUG = True