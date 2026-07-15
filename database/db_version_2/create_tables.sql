/* *************************************************************
 Drop and Create the tables for the grants_investigations database.
*************************************************************** */

-- Switch to grants_investigations database
USE `grants_investigations`

-- ----------------------------
-- Investigator TABLE
-- Drop the table if it exists
DROP TABLE IF EXISTS `investigators`;

-- Create the table
CREATE TABLE IF NOT EXISTS `investigators` (
    `id` int(11) NOT NULL,
    `first_name` varchar(25) NOT NULL,
    `middle_name` varchar(25) NOT NULL,
    `last_name` varchar(25) NOT NULL,
    `title` varchar(100) NOT NULL,
    `email` varchar(150) NOT NULL,
    `department` varchar(150) NOT NULL
);

-- Designate the `id` column as the primary key
ALTER TABLE `investigators`
    ADD PRIMARY KEY (`id`);

-- Make `id` column auto increment on inserts
ALTER TABLE `investigators`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- -------------------------------
-- GRANTS TABLE
-- Drop the table if it exists
DROP TABLE IF EXISTS `grants`;

-- Create the table
CREATE TABLE IF NOT EXISTS `grants` (
    `id` int(11) NOT NULL,
    `grant_name` varchar(100) NOT NULL,
    `status` varchar(50) NOT NULL,
    `funding_amount` int(9999999) NOT NULL
);

-- Add primary key
ALTER TABLE `grants`
    ADD PRIMARY KEY (`id`);

-- Make `id` column AUTO INCREMENT
ALTER TABLE `grants`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- ---------------------------------
-- GRANT_INVESTIGATOR_XREF TABLE
-- Drop grant_investigator_xref table if it exists
DROP TABLE IF EXISTS `grant_investigator_xref`;

-- Create grant_investigator_xref table
CREATE TABLE `grant_investigator_xref` (
    `investigator_id` int(11) NOT NULL,
    `grant_id` int(11) NOT NULL,
    `start_date` varchar(25) NOT NULL,
    `end_date` varchar(25) NOT NULL,
    `status` varchar(25) NOT NULL
);

-- Create indexes on employee_id and course_id columns
ALTER TABLE `grant_investigator_xref`
    ADD KEY `grant_investigator_xref_ibfk_1` (`investigator_id`),
    ADD KEY `grant_investigator_xref_ibfk_2` (`grant_id`);

-- Add Cascade Delete Constraint on employee_id column
ALTER TABLE `grant_investigator_xref`
    ADD CONSTRAINT `grant_investigator_ibfk_1`
    FOREIGN KEY (`investigator_id`) REFERENCES `investigators` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- Add Cascade Delete Constraint on course_id column
ALTER TABLE `grant_investigator_xref`
    ADD CONSTRAINT `grant_investigator_ibfk_2`
    FOREIGN KEY (`grant_id`) REFERENCES `grants` (`id`)
    ON UPDATE CASCADE;