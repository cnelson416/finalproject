"""Implements AppServices Class."""

from employee_training.application_base import ApplicationBase
from employee_training.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import json
import inspect
from typing import List, Dict

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)

    def get_all_employees_as_json(self)->str:
        """Returns all employees as JSON string"""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        try:
            results = self.DB.select_all_employees()
            return json.dumps(results)

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}') 