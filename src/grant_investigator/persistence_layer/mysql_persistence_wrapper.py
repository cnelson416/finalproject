"""Define the MySQLPersistenceWrapper class."""

from grant_investigator.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json
from typing import List
from grant_investigator.infrastructure_layer.investigator import Investigator
from grant_investigator.infrastructure_layer.grant import Grant
from enum import Enum
import sys

class MySQLPersistenceWrapper(ApplicationBase):
	"""Implement the MySQLPersistenceWrapper class."""

	def __init__(self, config:dict)->None:
		"""Initialize object."""
		self._config_dict = config
		self.META = config["meta"]
		self.DATABASE = config["database"]
		super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = \
			self.DATABASE["connection"]["config"]["database"]
		self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
		self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
		self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]

		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

		# Database Connection
		self._connection_pool = \
			self._initialize_database_connection_pool(self.DB_CONFIG)
		
		# Investigator Column ENUMS
		self.InvestigatorColumns = \
			Enum('InvestigatorColumns', [('id', 0), ('first_name', 1),
				('last_name', 2), ('email', 3), ('institution', 4)])

		# Grant Column ENUMS
		self.GrantColumns = \
			Enum('GrantColumns', [('grant_name', 0), ('grant_number', 1),
				('funding_agency', 2), ('funding_amount', 3), ('start_date', 4),
				('end_date', 5)])


		# SQL String Constants
		self.SELECT_ALL_INVESTIGATORS = \
			f"SELECT id, first_name, last_name, email, institution" \
			f"FROM investigators"
		
		self.SELECT_ALL_INVESTIGATORS_WITH_GRANTS = \
			f"SELECT `investigators`.id, first_name, last_name, grant_name, grant_number, funding_agency, funding_amount " \
				f"start_date, end_date, status " \
			f"FROM investigators, grants, grant_investigator_xref " \
			f"WHERE (`investigators`.id = investigator_id) AND (`grants`.id = grant_id)"

		self.SELECT_GRANTS_FOR_INVESTIGATOR_ID = \
			f"SELECT grant_name, grant_number, funding_agency, funding_amount, start_date, end_date " \
			f"FROM grants, grant_investigator_xref " \
			f"WHERE (investigator_id = %s) AND (`grants`.id = grant_id)"

		self.INSERT_INVESTIGATOR = \
			f"INSERT INTO investigators " \
			f"(first_name, last_name, email, institution" \
			f"values(%s, %s, %s, %s)"

		self.CHECK_FOR_PRIMARY_KEY_IN_INVESTIGATORS_TABLE = \
			f"SELECT id " \
			f"FROM investigators " \
			f"WHERE id = %s"

	# MySQLPersistenceWrapper Methods
	def select_all_investigators(self)->list[Investigator]:
		"""Returns a list of all investigator rows."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_INVESTIGATORS)
					results = cursor.fetchall()
					investigator_list = self._populate_investigator_objects(results)

					for investigator in investigator_list:
						grant_list = \
							self.select_all_grant_for_investigator_id(investigator.id)
						self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
							{grant_list}')
						investigator.grant = self._populate_grant_objects(grant_list)

			return investigator_list

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def select_all_investigators_with_grants(self)->list:
		"""Returns a list of all investigators rows with grants."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_INVESTIGATORS_WITH_GRANTS)
					results = cursor.fetchall()

			return results

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


	def select_all_grants_for_investigator_id(self, investigator_id:int) \
		->List[Grant]:
		"""Returns a list of grants rows for investigator id."""
		if not isinstance(investigator_id, int):
			raise TypeError(f'Invalid investigator_id argument type. Expected int.')
		if (investigator_id < 1) or (investigator_id > sys.maxsize):
			raise ValueError(f'investigator_id out of range. ')
		if not self._is_primary_key_in_investigators_table(investigator_id):
			raise ValueError(f'investigator_id not valid primary key.')

		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_GRANTS_FOR_INVESTIGATOR_ID,
					([investigator_id]))
					results = cursor.fetchall()

			return results

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def create_investigator(self, investigator:Investigator)->Investigator:
		"""Create a new record in the investigators table."""
		if not isinstance(investigator, Investigator):
			raise TypeError(f'Invalid investigator argument type. Expected Investigator.')
		if not investigator.is_valid():
			raise ValueError(f'investigator object not populated.')

		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_INVESTIGATOR,
						([investigator.first_name, investigator.last_name,
						investigator.email, investigator.institution]))
					connection.commit()
					self._logger.log_debug(f'Updated {cursor.rowcount} row.')
					self._logger.log_debug(f'Last Row ID: {cursor.lastrowid}.')
					investigator.id = cursor.lastrowid

			return investigator

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


		##### Private Utility Methods #####

	def _initialize_database_connection_pool(self, config:dict)->MySQLConnectionPool:
		"""Initializes database connection pool."""
		try:
			self._logger.log_debug(f'Creating connection pool...')
			cnx_pool = \
				MySQLConnectionPool(pool_name = self.DATABASE["pool"]["name"],
					pool_size=self.DATABASE["pool"]["size"],
					pool_reset_session=self.DATABASE["pool"]["reset_session"],
					use_pure=self.DATABASE["pool"]["use_pure"],
					**config)
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!')
			return cnx_pool
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem creating connection pool: {err}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Check DB cnfg:\n{json.dumps(self.DATABASE)}')
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Problem creating connection pool: {e}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Check DB conf:\n{json.dumps(self.DATABASE)}')


	def _populate_investigator_objects(self, results:List)->List[Investigator]:
		"""Populates and returns a list of Investigator objects."""
		investigator_list = []
		try:
			for row in results:
				investigator = Investigator()
				investigator.id = row[self.InvestigatorColumns['id'].value]
				investigator.first_name = row[self.InvestigatorColumns['first_name'].value]
				investigator.last_name = row[self.InvestigatorColumns['last_name'].value]
				investigator.last_name = row[self.InvestigatorColumns['email'].value]
				investigator.birthday = row[self.InvestigatorColumns['institution'].value]
				investigator_list.append(investigator)

			return investigator_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


	def _populate_grant_objects(self, results:List)->List[Grant]:
		"""Populates and returns a list of Grant objects."""
		grant_list = []
		try:
			for row in results:
				grant = Grant()
				grant.title = row[self.GrantColumns['grant_name'].value]
				grant.title = row[self.GrantColumns['grant_number'].value]
				grant.title = row[self.GrantColumns['funding_agency'].value]
				grant.title = row[self.GrantColumns['funding_amount'].value]
				grant.title = row[self.GrantColumns['start_date'].value]
				grant.title = row[self.GrantColumns['end_date'].value]
				grant_list.append(grant)

			return grant_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def _is_primary_key_in_investigators_table(self, id:int)->bool:
		"""Verifies primary key exists in investigators table."""
		return_value = False
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.CHECK_FOR_PRIMARY_KEY_IN_INVESTIGATORS_TABLE, \
						([id]))
					results = cursor.fetchall()
					if results:
						return_value = True
			return return_value

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')