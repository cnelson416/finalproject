"""Persistence Layer Unit Tests."""
from tests.context import MySQLPersistenceWrapper
from tests.context import Employee
from tests.context import Training
import pytest
import json
import os
from datetime import datetime

@pytest.fixture(scope="class")
def mysql_persistence_wrapper():
    print(f'\nSetting up mysql_persistence_wrapper_fixture...')
    working_dir = os.getcwd()
    config_dir = 'config'
    config_file_name = 'employee_training_app_config.json'
    config_dir_path = os.path.join(working_dir, config_dir, config_file_name )
    config_dict = None
    with open(config_dir_path, 'r') as f:
        config_dict = json.loads(f.read())
    db = MySQLPersistenceWrapper(config_dict)
    yield db
    print(f'\nTearing down mysql_persistence_wrapper_fixture...')


class TestPersistenceLayer:
    """Defines a group of related unit tests."""

    def test_select_all_employees(self, mysql_persistence_wrapper):
        employees_list = mysql_persistence_wrapper.select_all_employees()
        assert len(employees_list) > 0

    def test_select_employee_training(self, mysql_persistence_wrapper):
        training = mysql_persistence_wrapper.select_all_training_for_employee_id(1)
        assert len(training) > 0

    def test_create_employee(self, mysql_persistence_wrapper):
        employee = Employee()
        employee.first_name = 'Alex'
        employee.middle_name = 'J'
        employee.last_name = 'Remily'
        employee.gender = 'M'
        employee.birthday = datetime.strptime('1986/09/09', '%Y/%m/%d')
        employee = mysql_persistence_wrapper.create_employee(employee)
        assert employee.id > 0

     # Edge-Case Testing
    def test_select_employee_training_employee_id_none(self, mysql_persistence_wrapper):
        with pytest.raises(TypeError):
            training = mysql_persistence_wrapper.select_all_training_for_employee_id(None)

    def test_select_employee_training_employee_id_zero(self,
                mysql_persistence_wrapper):
        with pytest.raises(TypeError):
            training = mysql_persistence_wrapper.select_all_training_for_employee_id(0)

    def test_select_employee_training_employee__id_negative(self,
                mysql_persistence_wrapper):
        with pytest.raises(ValueError):
            training = \
                mysql_persistence_wrapper.select_all_training_for_employee_id(-1)

    def test_select_employee_training_employee_id_excessive(self,
            mysql_persistence_wrapper):
        with pytest.raises(ValueError):
            training = \
                mysql_persistence_wrapper.select_all_training_for_employee_id(100)

    def test_create_employee_with_default_values(self,
            mysql_persistence_wrapper):
        employee = Employee()
        with pytest.raises(ValueError):
            employee = mysql_persistence_wrapper.create_employee(employee)

    def test_create_employee_with_null_object(self, mysql_persistence_wrapper):
        employee = None
        with pytest.raises(TypeError):
            employee = mysql_persistence_wrapper.create_employee(employee)