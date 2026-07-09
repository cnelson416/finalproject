"""Defines the MySQLPersistenceWrapper class."""

from employee_training.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json
from typing import List
from employee_training.infrastructure_layer.employee import Employee
from employee_training.infrastructure_layer.training import Training
from enum import Enum

class MySQLPersistenceWrapper(ApplicationBase):
	"""Implements the MySQLPersistenceWrapper class."""

	def __init__(self, config:dict)->None:
		"""Initializes object. """
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
		
		# Employee Column ENUMS
		self.EmployeeColumns = \
			Enum('EmployeeColumns', [('id', 0), ('first_name', 1),
				('middle_name', 2), ('last_name', 3), ('birthday', 4),
				('gender', 5)])

		# Training Column ENUMS
		self.TrainingColumns = \
			Enum('TrainingColumns', [('title', 0), ('description', 1),
				('start_date', 2), ('end_date', 3), ('status', 4)])


		# SQL String Constants
		self.SELECT_ALL_EMPLOYEES = \
			f"SELECT id, first_name, middle_name, last_name, birthday, gender " \
			f"FROM employees"
		
		self.SELECT_ALL_EMPLOYEES_WITH_TRAINING = \
			f"SELECT `employees`.id, first_name, last_name, title, description, " \
				f"start_date, end_date, status " \
			f"FROM employees, courses, employee_training_xref " \
			f"WHERE (`employees`.id = employee_id) AND (`courses`.id = course_id)"

		self.SELECT_TRAINING_FOR_EMPLOYEE_ID = \
			f"SELECT title, description, start_date, end_date, status " \
			f"FROM courses, employee_training_xref " \
			f"WHERE (employee_id = %s) AND (`courses`.id = course_id)"




	# MySQLPersistenceWrapper Methods
	def select_all_employees(self)->list:
		"""Returns a list of all employee rows."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_EMPLOYEES)
					results = cursor.fetchall()
					employee_list = self._populate_employee_objects(results)

					for employee in employee_list:
						training_list = \
							self.select_all_training_for_employee_id(employee.id)
						self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
							{training_list}')
						employee.training = self._populate_training_objects(training_list)

			return employee_list

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def select_all_employees_with_training(self)->list:
		"""Returns a list of all employee rows with training."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_EMPLOYEES_WITH_TRAINING)
					results = cursor.fetchall()

			return results

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


	def select_all_training_for_employee_id(self, employee_id:int) \
		->List[Training]:
		"""Returns a list of training rows for employee id."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_TRAINING_FOR_EMPLOYEE_ID,
					([employee_id]))
					results = cursor.fetchall()

			return results

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


	def _populate_employee_objects(self, results:List)->List[Employee]:
		"""Populates and returns a list of Employee objects."""
		employee_list = []
		try:
			for row in results:
				employee = Employee()
				employee.id = row[self.EmployeeColumns['id'].value]
				employee.first_name = row[self.EmployeeColumns['first_name'].value]
				employee.middle_name = \
					row[self.EmployeeColumns['middle_name'].value]
				employee.last_name = row[self.EmployeeColumns['last_name'].value]
				employee.birthday = row[self.EmployeeColumns['birthday'].value]
				employee.gender = row[self.EmployeeColumns['gender'].value]
				employee_list.append(employee)

			return employee_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


	def _populate_training_objects(self, results:List)->List[Training]:
		"""Populates and returns a list of Training objects."""
		training_list = []
		try:
			for row in results:
				training = Training()
				training.title = row[self.TrainingColumns['title'].value]
				training.description = \
					row[self.TrainingColumns['description'].value]
				training.start_date = row[self.TrainingColumns['start_date'].value]
				training.end_date = row[self.TrainingColumns['end_date'].value]
				training.status = row[self.TrainingColumns['status'].value]
				training_list.append(training)

			return training_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')