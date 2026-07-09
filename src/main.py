"""Entry point for the Employee Training Application."""

import json
from argparse import ArgumentParser
#from employee_training.presentation_layer.user_interface import UserInterface
#from employee_training.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from employee_training.service_layer.app_services import AppServices

def main():
	"""Entry point."""
	args = configure_and_parse_commandline_arguments()

	if args.configfile:
		config = None
		with open(args.configfile, 'r') as f:
			config = json.loads(f.read())

		service_layer = AppServices(config)
		employees_list = service_layer.get_all_employees_as_json()
		print(employees_list)

#	ui = UserInterface(config)
#	ui.start()
			
		


def configure_and_parse_commandline_arguments():
	"""Configure and parse command-line arguments."""
	parser = ArgumentParser(
	prog='main.py',
	description='Start the Employee Training application with a configuration file.',
	epilog='POC: Chris Nelson | cnelson416@gmail.com')

	parser.add_argument('-c','--configfile',
					help="Configuration file to load.",
					required=True)
	args = parser.parse_args()
	return args



if __name__ == "__main__":
	main()