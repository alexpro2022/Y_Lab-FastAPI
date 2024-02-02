from uuid import uuid4

import pytest

from ...generic_db_repo.testing_lib import BaseCRUDTest
from .fixtures.data import BaseCRUD, CRUDExec, CRUDScalars, Data, Model


class TestBaseCRUD:
    """Testing only hooks exceptions."""
    crud = BaseCRUD
    create_data = Data.create_payload

    @pytest.fixture
    def get_crud(self, init_db, get_test_session):
        return BaseCRUD(Model, get_test_session)

    @pytest.mark.parametrize('method_name', ('update', 'delete'))
    async def test_base_crud_raises_has_perimission_exc(self, get_crud, monkeypatch, method_name):
        async def async_dummy_mock(*args, **kwargs):
            pass

        monkeypatch.setattr(BaseCRUD, '_BaseCRUD__get_or_404', async_dummy_mock)
        with pytest.raises(NotImplementedError, match='Method `has_permission` must be implemented.'):
            await get_crud.__getattribute__(method_name)(id=uuid4())

    @pytest.mark.parametrize('method_name, error_msg', (
        ('update', 'Method `is_update_allowed` must be implemented.'),
        ('delete', 'Method `is_delete_allowed` must be implemented.'),
    ))
    async def test_base_crud_raises_is_allowed_exc(self, get_crud, monkeypatch, method_name, error_msg):
        async def async_dummy_mock(*args, **kwargs):
            pass

        def dummy_mock(*args, **kwargs):
            pass

        monkeypatch.setattr(BaseCRUD, '_BaseCRUD__get_or_404', async_dummy_mock)
        monkeypatch.setattr(BaseCRUD, 'has_permission', dummy_mock)
        with pytest.raises(NotImplementedError, match=error_msg):
            await get_crud.__getattribute__(method_name)(id=uuid4())


class TestCRUDScalars(BaseCRUDTest):
    msg_already_exists = 'Scalars_exists.'
    msg_not_found = 'Scalars_not_found.'
    model = Model
    crud = CRUDScalars
    create_data = Data.create_payload
    update_data = Data.update_payload


class TestCRUDExec(BaseCRUDTest):
    msg_already_exists = 'Exec_exists.'
    msg_not_found = 'Exec_not_found.'
    model = Model
    crud = CRUDExec
    create_data = Data.create_payload
    update_data = Data.update_payload
