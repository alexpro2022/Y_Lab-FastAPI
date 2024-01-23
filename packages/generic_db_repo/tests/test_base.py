from .conftest import Base


class BaseTest(Base):
    pass


def test_base():
    base = BaseTest()
    assert base.__tablename__ == 'basetest'
    assert hasattr(base, 'id')
    assert base.id is None
    assert repr(base) == '\nid: None'
