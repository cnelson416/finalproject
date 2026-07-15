/* ******************************************
 Drop and create the employee_training_user
********************************************/

-- Drop user if exists
DROP USER IF EXISTS 'employee_training_user'@'%';

-- Create user if not exists
CREATE USER IF NOT EXISTS 'employee_training_user'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'employee_training_user'@'%';
ALTER USER 'employee_training_user'@'%'
    REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0
    MAX_CONNECTIONS_PER_HOUR 0
    MAX_UPDATES_PER_HOUR 0
    MAX_USER_CONNECTIONS 0;
GRANT ALL PRIVILEGES ON `employee\_training\_user\_%`.*
    TO 'employee_training_user'@'%';
GRANT ALL PRIVILEGES ON `employee\_training`.*
    TO 'employee_training_user'@'%' WITH GRANT OPTION;