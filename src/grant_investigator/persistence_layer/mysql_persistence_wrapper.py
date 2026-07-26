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
			Enum('GrantColumns', [('id', 0), ('grant_name', 1), ('grant_number', 2),
				('funding_agency', 3), ('funding_amount', 4), ('start_date', 5),
				('end_date', 6)])


		# SQL String Constants
		self.SELECT_ALL_INVESTIGATORS = \
			f"SELECT id, first_name, last_name, email, institution " \
			f"FROM investigators"

		self.SELECT_ALL_GRANTS = \
			f"SELECT id, grant_name, grant_number, funding_agency, funding_amount, start_date, end_date " \
			f"FROM grants"
		
		self.SELECT_ALL_INVESTIGATORS_WITH_GRANTS = \
			f"SELECT `investigators`.id, first_name, last_name, grant_name, grant_number, funding_agency, funding_amount, " \
				f"start_date, end_date " \
			f"FROM investigators, grants, grant_investigator_xref " \
			f"WHERE (`investigators`.id = investigator_id) AND (`grants`.id = grant_id)"

		self.SELECT_GRANTS_FOR_INVESTIGATOR_ID = \
			f"SELECT grants.id, grant_name, grant_number, funding_agency, funding_amount, start_date, end_date " \
			f"FROM grants, grant_investigator_xref " \
			f"WHERE (investigator_id = %s) AND (`grants`.id = grant_id)"

		self.SELECT_INVESTIGATORS_FOR_GRANT_ID = \
			f"SELECT investigators.id, first_name, last_name, email, institution " \
			f"FROM investigators, grant_investigator_xref " \
			f"WHERE (grant_id = %s) AND (`investigators`.id = investigator_id)"

		self.INSERT_INVESTIGATOR = \
			f"INSERT INTO investigators " \
			f"(first_name, last_name, email, institution) " \
			f"VALUES (%s, %s, %s, %s)"
	
		self.CHECK_FOR_PRIMARY_KEY_IN_INVESTIGATORS_TABLE = \
			f"SELECT id " \
			f"FROM investigators " \
			f"WHERE id = %s"

		self.CHECK_FOR_PRIMARY_KEY_IN_GRANTS_TABLE = \
			f"SELECT id " \
			f"FROM grants " \
			f"WHERE id = %s"

		self.INSERT_GRANT = \
			f"INSERT INTO grants " \
			f"(grant_name, grant_number, funding_agency, funding_amount, start_date, end_date) " \
			f"VALUES (%s, %s, %s, %s, %s, %s)"

		self.INSERT_INVESTIGATOR_GRANT_XREF = \
			f"INSERT INTO grant_investigator_xref (investigator_id, grant_id) " \
			f"VALUES (%s, %s)"

		self.DELETE_INVESTIGATOR_GRANT_XREF = \
			f"DELETE FROM grant_investigator_xref " \
			f"WHERE (investigator_id = %s) AND (grant_id = %s)"

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
						grant_list = self.select_all_grants_for_investigator_id(investigator.id)
						self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: {grant_list}')
						investigator.grants = self._populate_grant_objects(grant_list)

			return investigator_list

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def select_all_grants(self)->list[Grant]:
		"""Returns a list of all grant rows."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_GRANTS)
					results = cursor.fetchall()
					grant_list = self._populate_grant_objects(results)
					
					for grant in grant_list:
						investigator_list = self.select_all_investigators_with_grants_id(grant.id)
						self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: {investigator_list}')
						grant.investigators = self._populate_investigator_objects(investigator_list)
					
			return grant_list

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

	def select_all_investigators_with_grants_id(self, grant_id:int) \
		->List[Investigator]:
		"""Returns a list of investigators rows for grant id."""
		if not isinstance(grant_id, int):
			raise TypeError(f'Invalid grant_id argument type. Expected int.')
		if (grant_id < 1) or (grant_id > sys.maxsize):
			raise ValueError(f'grant_id out of range. ')
		if not self._is_primary_key_in_grants_table(grant_id):
			raise ValueError(f'grant_id not valid primary key.')

		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_INVESTIGATORS_FOR_GRANT_ID,
					([grant_id]))
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
					([
						investigator.first_name, 
						investigator.last_name, 
						investigator.email, 
						investigator.institution
					]))
					connection.commit()
					self._logger.log_debug(f'Updated {cursor.rowcount} row.')
					self._logger.log_debug(f'Last Row ID: {cursor.lastrowid}.')
					investigator.id = cursor.lastrowid

			return investigator

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def create_grant(self, grant:Grant)->Grant:
		"""Create a new record in the grants table."""
		if not isinstance(grant, Grant):
			raise TypeError(f'Invalid grant argument type. Expected Grant.')
		if not grant.is_valid():
			raise ValueError(f'grant object not populated.')

		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_GRANT, 
					([
						grant.grant_name, 
						grant.grant_number, 
						grant.funding_agency, 
						grant.funding_amount,
						grant.start_date,
						grant.end_date
					]))
					connection.commit()
					self._logger.log_debug(f'Updated {cursor.rowcount} row.')
					self._logger.log_debug(f'Last Row ID: {cursor.lastrowid}.')
					grant.id = cursor.lastrowid

			return grant

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


	def insert_investigator_grant_xref(self, investigator_id:int, grant_id:int) -> None:
		"""Insert a row connecting an investigator to a grant."""
		if not isinstance(investigator_id, int):
			raise TypeError(f'Invalid investigator_id argument type. Expected int.')
		if not isinstance(grant_id, int):
			raise TypeError(f'Invalid grant_id argument type. Expected int.')
		if (investigator_id < 1) or (investigator_id > sys.maxsize):
			raise ValueError(f'investigator_id out of range.')
		if (grant_id < 1) or (grant_id > sys.maxsize):
			raise ValueError(f'grant_id out of range.')
		if not self._is_primary_key_in_investigators_table(investigator_id):
			raise ValueError(f'investigator_id not valid primary key.')
		if not self._is_primary_key_in_grants_table(grant_id):
			raise ValueError(f'grant_id not valid primary key.')

		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_INVESTIGATOR_GRANT_XREF,
						(investigator_id, grant_id))
				connection.commit()

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def delete_investigator_grant_xref(self, investigator_id:int, grant_id:int) -> None:
		"""Removes the row connecting an investigator to a grant."""
		if not isinstance(investigator_id, int):
			raise TypeError(f'Invalid investigator_id argument type. Expected int.')
		if not isinstance(grant_id, int):
			raise TypeError(f'Invalid grant_id argument type. Expected int.')
		if (investigator_id < 1) or (investigator_id > sys.maxsize):
			raise ValueError(f'investigator_id out of range.')
		if (grant_id < 1) or (grant_id > sys.maxsize):
			raise ValueError(f'grant_id out of range.')
		if not self._is_primary_key_in_investigators_table(investigator_id):
			raise ValueError(f'investigator_id not valid primary key.')
		if not self._is_primary_key_in_grants_table(grant_id):
			raise ValueError(f'grant_id not valid primary key.')

		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.DELETE_INVESTIGATOR_GRANT_XREF,
						(investigator_id, grant_id))
					rows_affected = cursor.rowcount
				connection.commit()

			if rows_affected == 0:
				self._logger.log_debug(
					f'{inspect.currentframe().f_code.co_name}: '
					f'no xref row found for investigator_id={investigator_id}, grant_id={grant_id}')

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
				investigator.email = row[self.InvestigatorColumns['email'].value]
				investigator.institution = row[self.InvestigatorColumns['institution'].value]
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
				grant.id = row[self.GrantColumns['id'].value]
				grant.grant_name = row[self.GrantColumns['grant_name'].value]
				grant.grant_number = row[self.GrantColumns['grant_number'].value]
				grant.funding_agency = row[self.GrantColumns['funding_agency'].value]
				grant.funding_amount = row[self.GrantColumns['funding_amount'].value]
				grant.start_date = row[self.GrantColumns['start_date'].value]
				grant.end_date = row[self.GrantColumns['end_date'].value]
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

	def _is_primary_key_in_grants_table(self, id:int)->bool:
		"""Verifies primary key exists in grants table."""
		return_value = False
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.CHECK_FOR_PRIMARY_KEY_IN_GRANTS_TABLE, \
						([id]))
					results = cursor.fetchall()
					if results:
						return_value = True
			return return_value

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')