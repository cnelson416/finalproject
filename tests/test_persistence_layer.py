"""Persistence Layer Unit Tests."""
from tests.context import MySQLPersistenceWrapper
from tests.context import Investigator
from tests.context import Grant
import pytest
import json
import os
from datetime import datetime

@pytest.fixture(scope="class")
def mysql_persistence_wrapper():
    print(f'\nSetting up mysql_persistence_wrapper_fixture...')
    working_dir = os.getcwd()
    config_dir = 'config'
    config_file_name = 'grant_investigator_app_config.json'
    config_dir_path = os.path.join(working_dir, config_dir, config_file_name )
    config_dict = None
    with open(config_dir_path, 'r') as f:
        config_dict = json.loads(f.read())
    db = MySQLPersistenceWrapper(config_dict)
    yield db
    print(f'\nTearing down mysql_persistence_wrapper_fixture...')


class TestPersistenceLayer:
    """Defines a group of related unit tests."""

    def test_select_all_investigators(self, mysql_persistence_wrapper):
        investigator_list = mysql_persistence_wrapper.select_all_investigators()
        assert len(investigator_list) > 0

    def test_select_investigator_grants(self, mysql_persistence_wrapper):
        grants = mysql_persistence_wrapper.select_all_grants_for_investigator_id(1)
        assert len(grants) > 0

    def test_create_investigator(self, mysql_persistence_wrapper):
        investigator = Investigator()
        investigator.first_name = 'Alex'
        investigator.last_name = 'Remily'
        investigator.email = 'ARemily12345@gmail.com'
        investigator.institution = 'Business Institution of Tests'
        investigator = mysql_persistence_wrapper.create_employee(investigator)
        assert investigator.id > 0

     # Edge-Case Testing
    def test_select_investigator_grant_investigator_id_none(self, mysql_persistence_wrapper):
        with pytest.raises(TypeError):
            grants = mysql_persistence_wrapper.select_all_grants_for_investigator_id(None)

    def test_select_investigator_grant_investigator_id_zero(self,
                mysql_persistence_wrapper):
        with pytest.raises(TypeError):
            grants = mysql_persistence_wrapper.select_all_grants_for_investigator_id(0)

    def test_select_investigator_grants_investigator_id_negative(self,
                mysql_persistence_wrapper):
        with pytest.raises(ValueError):
            grants = \
                mysql_persistence_wrapper.select_all_grants_for_investigator_id(-1)

    def test_select_investigator_grant_investigator_id_excessive(self,
            mysql_persistence_wrapper):
        with pytest.raises(ValueError):
            grants = \
                mysql_persistence_wrapper.select_all_grants_for_investigator_id(100)

    def test_create_investigator_with_default_values(self,
            mysql_persistence_wrapper):
        investigator = Investigator()
        with pytest.raises(ValueError):
            investigator = mysql_persistence_wrapper.create_investigator(investigator)

    def test_create_investigator_with_null_object(self, mysql_persistence_wrapper):
        investigator = None
        with pytest.raises(TypeError):
            investigator = mysql_persistence_wrapper.create_investigator(investigator)