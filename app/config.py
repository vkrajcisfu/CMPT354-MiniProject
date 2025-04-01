import os

class Config:
    SECRET_KEY = os.environ.get('secret354key') or 'you-will-never-guess'