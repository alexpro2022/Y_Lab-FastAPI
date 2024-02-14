from app.celery_tasks.wb_loaders import google_load_workbook, local_load_workbook


def test_local_load_workbook():
    res = local_load_workbook()
    print(*res)
    assert 0


async def test_google_load_workbook():
    res = await google_load_workbook()
    print(*res)
    assert 0
