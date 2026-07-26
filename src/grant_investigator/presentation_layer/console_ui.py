"""Contains the definition for a ConsoleUI class."""

from grant_investigator.service_layer.app_services import AppServices
from grant_investigator.application_base import ApplicationBase
from grant_investigator.infrastructure_layer.investigator import Investigator
from grant_investigator.infrastructure_layer.grant import Grant
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
        print(f"\n\n\t\tGrant Investigator Application Menu")
        print()
        print(f"\t1. List Investigators")
        print(f"\t2. List Grants")
        print(f"\t3. Add Investigator")
        print(f"\t4. Record Investigator Grants")
        print(f"\t5. Add Grant")
        print(f"\t6. Exit")
        print()

    def process_menu_choice(self)->None:
        """Processes users menu choice."""
        menu_choice = input("\tMenu Choice: ")
        match menu_choice[0]:
            case '1': self.list_investigators()
            case '2': self.list_grants()
            case '3': self.add_investigator()
            case '4': self.record_investigator_grants()
            case '5': self.add_grant()
            case '6': sys.exit()
            case _: print(f"Invalid Menu Choice {menu_choice[0]}")

    def list_investigators(self)->None:
        """List investigators."""
        investigators = self.app_services.get_all_investigators()
        investigators_table = PrettyTable()
        investigators_table.field_names = ['id', 'First Name', 'Last Name',
                                    'Email', 'Institution', 'Grants']
        grants_table = PrettyTable()
        grants_table.field_names = ['Grant Name', 'Funding Amount']
        grants_table.align = 'l'
        for investigator in investigators:
            for grant in investigator.grants:
                grants_table.add_row([grant.grant_name, grant.funding_amount])

                investigators_table.add_row([investigator.id, investigator.first_name,
                                    investigator.last_name, investigator.email,
                                    investigator.institution, 
                                    grants_table.get_string()])
                investigators_table.add_divider()
                grants_table.clear_rows()
        print(investigators_table)

    def list_grants(self)->None:
        """List grants."""
        print("list_grants() method stub called...")

    def add_investigator(self)->None:
        """Add investigator."""
        print("\n\tAdd Investigator...")
        investigator = Investigator()
        try:
            investigator.first_name = input('First Name: ')
            investigator.last_name = input('Last Name: ')
            investigator.email = input('Email: ')
            investigator.institution = input('Institution: ')
            investigator = self.app_services.create_investigator(investigator=investigator)
            print(f'New investigator id: {investigator.id}')

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: ' \
                                f'{e}')

    def record_investigator_grant(self)->None:
        """Record investigator grant."""
        print("record_investigator_grant() method stub called...")

    def add_grant(self)->None:
        """Add grant."""
        print("\n\tAdd Grant...")
        grant = Grant()
        try:
            grant.grant_name = input('Grant Name: ')
            grant.grant_number = input('Grant Number: ')
            grant.funding_amount = input('Funding Amount: ')
            grant.funding_agency = input('Funding Agency: ')
            start_date_input = input('Start Date (mm/dd/yyyy): ')
            grant.start_date = datetime.strptime(start_date_input, '%m/%d/%Y')
            end_date_input = input('End Date (mm/dd/yyyy): ')
            grant.end_date = datetime.strptime(end_date_input, '%m/%d/%Y')
            grant = self.app_services.create_grant(grant=grant)
            print(f'New grant id: {grant.id}')

        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: ' \
                                f'{e}')    

    def start(self)->None:
        while True:
            self.display_menu()
            self.process_menu_choice()