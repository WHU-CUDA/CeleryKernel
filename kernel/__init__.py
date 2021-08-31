from celery import Celery

app = Celery("kernel")
app.config_from_object('kernel.celery_config')
