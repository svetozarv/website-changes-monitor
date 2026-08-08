import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

# use the variables defined in the .env file (when the project is running locally and the .env file is present)
load_dotenv()

# uses environment variables defined in the host environment (where the .env file is not present, f.e. Docker)
REDIS_PORT = os.getenv('REDIS_PORT')


celery_instance = Celery(main="website_changes_monitor", broker="redis://redis:6379/0",
                         backend="redis://redis:6379/0")
celery_instance.autodiscover_tasks(["core"])


celery_instance.conf.beat_schedule = {
    "ping-all-active": {
        "task": "core.tasks.schedule_pings",
        "schedule": crontab(minute="*")
    }
}
