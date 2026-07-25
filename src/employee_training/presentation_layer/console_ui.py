"""Contains the definition for a ConsoleUI class."""

from employee_training.service_layer.app_services import AppServices
from employee_training.application_base import ApplicationBase
from employee_training.infrastructure_layer.employee import Employee
from prettytable import PrettyTable
from datetime import datetime
import sys
import inspect



class ConsoleUI(ApplicationBase):
    """Defines the ConsoleUI class."""
    def __init__(self, config:dict)->None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"])
        self.app_services = AppServices(config)


    # Public Methods
    def display_menu(self)->None:
        """Display the menu."""
        print(f"\n\n\t\tEmployee Training Application Menu")
        print()
        print(f"\t1. List Employees")
        print(f"\t2. List Courses")
        print(f"\t3. Add Employee")
        print(f"\t4. Record Employee Training")
        print(f"\t5. Add Course")
        print(f"\t6. Exit")
        print()

    def process_menu_choice(self)->None:
        """Processes users menu choice."""
        menu_choice = input("\tMenu Choice: ")
        match menu_choice[0]:
            case '1': self.list_employees()
            case '2': self.list_courses()
            case '3': self.add_employee()
            case '4': self.record_employee_training()
            case '5': self.add_course()
            case '6': sys.exit()
            case _: print(f"Invalid Menu Choice {menu_choice[0]}")

    def list_employees(self)->None:
        """List employees."""
        employees = self.app_services.get_all_employees()
        employee_table = PrettyTable()
        employee_table.field_names = ['id', 'First Name', 'Middle Name',
                                    'Last Name', 'Gender', 'Birthday', 'Training']
        training_table = PrettyTable()
        training_table.field_names = ['Title', 'Status']
        training_table.align = 'l'
        for employee in employees:
            for training in employee.training:
                training_table.add_row([training.title, training.status])

                employee_table.add_row([employee.id, employee.first_name,
                                    employee.middle_name, employee.last_name,
                                    employee.gender, employee.birthday,
                                    training_table.get_string()])
                employee_table.add_divider()
                training_table.clear_rows()
        print(employee_table)

    def list_courses(self)->None:
        """List courses."""
        print("list_courses() method stub called...")

    def add_employee(self)->None:
        """Add employee."""
        print("\n\tAdd Employee...")
        employee = Employee()
        try:
            employee.first_name = input('First Name: ')
            employee.middle_name = input('Middle Name: ')
            employee.last_name = input('Last Name: ')
            employee.gender = input('Gender (M/F): ')
            birthday_input = input('Birthday (mm/dd/yyyy): ')
            employee.birthday = datetime.strptime(birthday_input, '%m/%d/%Y')
            employee = self.app_services.create_employee(employee=employee)
            print(f'New employee id: {employee.id}')

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: ' \
                                f'{e}')

    def record_employee_training(self)->None:
        """Record employee training."""
        print("record_employee_training() method stub called...")

    def add_course(self)->None:
        """Add course."""
        print("add_course() method stub called...")

    def start(self)->None:
        while True:
            self.display_menu()
            self.process_menu_choice()