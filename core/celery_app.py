from celery import Celery
from celery.schedules import crontab


celery_instance = Celery(main="website_changes_monitor", broker="redis://localhost:6379/0",
                         backend="redis://localhost:6379/0")
celery_instance.autodiscover_tasks(["core"])


celery_instance.conf.beat_schedule = {
    "ping-all-active": {
        "task": "core.tasks.schedule_pings",
        "schedule": crontab(minute="*")
    }
}
