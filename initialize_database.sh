 #!/bin/bash

# create logs directory if not there
echo 'Creating logs directory if it does not already exist...'
mkdir -p logs
echo 'Deleting old log files if they exist...'
rm -f logs/*

d=$(date)
echo $d

# Create db_version_2 - grant_investigators Database
echo "Running DB Version 2 Scripts..."
echo $d': Creating database...' | tee -a logs/create_database.log
mysql < database/db_version_2/create_database.sql 2>&1 | tee -a database/logs/create_database.log
echo $d': Creating user...' | tee -a logs/create_user.log
mysql < database/db_version_2/create_user.sql 2>&1 | tee -a database/logs/create_user.log
echo $d': Creating tables...' | tee -a logs/create_tables.log
mysql < database/db_version_2/create_tables.sql 2>&1 | tee -a database/logs/create_tables.log
echo $d': Inserting test data...' | tee -a logs/insert_test_data.log
mysql < database/db_version_2/insert_test_data.sql 2>&1 | tee -a database/logs/insert_test_data.log