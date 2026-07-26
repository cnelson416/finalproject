import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                            '../src/')))
from grant_investigator.persistence_layer.mysql_persistence_wrapper \
    import MySQLPersistenceWrapper
from grant_investigator.service_layer.app_services import AppServices
from grant_investigator.infrastructure_layer.investigator import Investigator
from grant_investigator.infrastructure_layer.grant import Grant