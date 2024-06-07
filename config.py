import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOAD_FOLDER = '/app/UPLOAD_FOLDER'

    SECRET_KEY = os.environ.get('SECRET_KEY') or '46b74dc7229cda8e0de864283dd32b07ed850f59f97aa1e209fedabf28c81283'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://std_2435_exam:ktHrF1978@std-mysql.ist.mospolytech.ru/std_2435_exam'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
