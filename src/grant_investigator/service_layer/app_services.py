"""Implements AppServices Class."""

from grant_investigator.application_base import ApplicationBase
from grant_investigator.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import json
import inspect
from grant_investigator.infrastructure_layer.investigator import Investigator
from typing import List, Dict

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initialize object."""
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)

    def get_all_investigators_as_json(self)->str:
        """Return all investigators as JSON string."""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        try:
            results = self.DB.select_all_investigators()
            return json.dumps(results)

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}') 

    def get_all_investigators(self)->List[Investigator]:
        """Return a list of investigator objects."""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        investigator_dict = {}
        investigator_dict['investigators'] = []

        try:
            results = self.DB.select_all_investigators()
            return results

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')

    def create_investigator(self, investigator:Investigator)->Investigator:
        """Create a new investigator in the database."""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        try:
            results = self.DB.create_investigator(investigator)
            return results

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
