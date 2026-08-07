from celery import Celery

celery_instance = Celery(main="website_changes_monitor", broker="redis://localhost:6379/0",
                         backend="redis://localhost:6379/0")
celery_instance.autodiscover_tasks(["core"])