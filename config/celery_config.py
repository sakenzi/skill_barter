from celery import Celery


app = Celery(
    'skill_berter',
    broker='redis://localhost:6379/0',
    backend='redis://locahost:6379/1'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)