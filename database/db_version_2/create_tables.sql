/* *************************************************************
 Drop and Create the tables for the grants_investigators database.
*************************************************************** */

-- Switch to grants_investigations database
USE `grants_investigators`

-- ----------------------------
-- Investigator TABLE
-- Drop the table if it exists
DROP TABLE IF EXISTS `investigators`;

-- Create the table
CREATE TABLE IF NOT EXISTS `investigators` (
    `id` int(11) NOT NULL,
    `first_name` varchar(25) NOT NULL,
    `last_name` varchar(25) NOT NULL,
    `email` varchar(150) UNIQUE NOT NULL,
    `institution` varchar(255) NOT NULL
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
    `grant_number` varchar(100) UNIQUE NOT NULL,
    `funding_agency` varchar(155) NOT NULL,
    `funding_amount` DECIMAL(12, 2) NOT NULL,
    `start_date` DATE,
    `end_date` DATE
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
    `role` varchar(100) DEFAULT 'Co-Investigator',
    `grant_percent` DECIMAL(5, 2) DEFAULT 0.00
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