/* ******************************************
 Drop and create the grant_investigator_user
********************************************/

-- Drop user if exists
DROP USER IF EXISTS 'grant_investigator_user'@'%';

-- Create user if not exists
CREATE USER IF NOT EXISTS 'grant_investigator_user'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'grant_investigator_user'@'%';
ALTER USER 'grant_investigator_user'@'%'
    REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0
    MAX_CONNECTIONS_PER_HOUR 0
    MAX_UPDATES_PER_HOUR 0
    MAX_USER_CONNECTIONS 0;
GRANT ALL PRIVILEGES ON `grant\_investigator\_user\_%`.*
    TO 'grant_investigator_user'@'%';
GRANT ALL PRIVILEGES ON `grant\_investigator`.*
    TO 'grant_investigator_user'@'%' WITH GRANT OPTION;