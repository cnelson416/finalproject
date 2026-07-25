import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                            '../src/')))
from employee_training.persistence_layer.mysql_persistence_wrapper \
    import MySQLPersistenceWrapper
from employee_training.service_layer.app_services import AppServices
from employee_training.infrastructure_layer.employee import Employee
from employee_training.infrastructure_layer.training import Training