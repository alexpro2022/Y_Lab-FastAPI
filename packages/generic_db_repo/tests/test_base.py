from ...generic_db_repo.base import Base


def test_base():
    class BaseTest(Base):
        pass

    base = BaseTest()
    assert base.__tablename__ == 'basetest'
    assert hasattr(base, 'id')
    assert base.id is None
    assert repr(base) == '\nid: None'
