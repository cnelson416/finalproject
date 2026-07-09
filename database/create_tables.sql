/* *************************************************************
 Drop and Create the tables for the employee_training database.
*************************************************************** */

-- Switch to employee_training database
USE `employee_training`

-- ----------------------------
-- EMPLOYEES TABLE
-- Drop the table if it exists
DROP TABLE IF EXISTS `employees`;

-- Create the table
CREATE TABLE IF NOT EXISTS `employees` (
    `id` int(11) NOT NULL,
    `first_name` varchar(25) NOT NULL,
    `middle_name` varchar(25) NOT NULL,
    `last_name` varchar(25) NOT NULL,
    `birthday` varchar(25) NOT NULL,
    `gender` char(1) NOT NULL
);

-- Designate the `id` column as the primary key
ALTER TABLE `employees`
    ADD PRIMARY KEY (`id`);

-- Make `id` column auto increment on inserts
ALTER TABLE `employees`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- -------------------------------
-- COURSES TABLE
-- Drop the table if it exists
DROP TABLE IF EXISTS `courses`;

-- Create the table
CREATE TABLE IF NOT EXISTS `courses` (
    `id` int(11) NOT NULL,
    `title` varchar(100) NOT NULL,
    `description` varchar(250) NOT NULL
);

-- Add primary key
ALTER TABLE `courses`
    ADD PRIMARY KEY (`id`);

-- Make `id` column AUTO INCREMENT
ALTER TABLE `courses`
    MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

-- ---------------------------------
-- EMPLOYEE_TRAINING_XREF TABLE
-- Drop employee_training_xref table if it exists
DROP TABLE IF EXISTS `employee_training_xref`;

-- Create employee_training table
CREATE TABLE `employee_training_xref` (
    `employee_id` int(11) NOT NULL,
    `course_id` int(11) NOT NULL,
    `start_date` varchar(25) NOT NULL,
    `end_date` varchar(25) NOT NULL,
    `status` varchar(25) NOT NULL
);

-- Create indexes on employee_id and course_id columns
ALTER TABLE `employee_training_xref`
    ADD KEY `employee_training_xref_ibfk_1` (`employee_id`),
    ADD KEY `employee_training_xref_ibfk_2` (`course_id`);

-- Add Cascade Delete Constraint on employee_id column
ALTER TABLE `employee_training_xref`
    ADD CONSTRAINT `employee_training_ibfk_1`
    FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- Add Cascade Delete Constraint on course_id column
ALTER TABLE `employee_training_xref`
    ADD CONSTRAINT `employee_training_ibfk_2`
    FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`)
    ON UPDATE CASCADE;