SECRET_KEY = 'thisisasecretkey'
SQLALCHEMY_DATABASE_URI = 'postgres://username:password@localhost/favifinddb'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'