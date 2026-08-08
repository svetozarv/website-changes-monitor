import requests
from db.database import SessionLocal
from db.models import CheckLog
from core.celery_app import celery_instance
from typing import Annotated

@celery_instance.task
def ping_url(target_id: int, url: str) -> Annotated[int, "status code"]:
    status_code = 0
    response_time_ms = 0

    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code,
        response_time_ms = int(response.elapsed.total_seconds() * 1000)
    except requests.RequestException as e:
        pass

    with SessionLocal() as db:
        check_log = CheckLog(target_id=target_id, status_code=status_code, response_time_ms=response_time_ms)
        db.add(check_log)
        db.commit()

    return status_code
