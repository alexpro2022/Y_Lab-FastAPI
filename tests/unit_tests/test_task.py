from app.celery_tasks.utils import periodic_task, get_rows


def test_periodic_task():
    result = periodic_task()
    print(result)
    assert 0
