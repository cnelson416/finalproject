SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

USE `employee_training`;

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE IF NOT EXISTS `courses` (
    `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` varchar(100) NOT NULL,
    `description` varchar(250) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Store course data.';

--
-- RELATIONSHIPS FOR TABLE `courses`:
--

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE IF NOT EXISTS `employees` (
    `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `first_name` varchar(25) NOT NULL,
    `middle_name` varchar(25) NOT NULL,
    `last_name` varchar(25) NOT NULL,
    `birthday` varchar(25) NOT NULL,
    `gender` char(1) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Store employee data.';

--
-- RELATIONSHIPS FOR TABLE `employees`:
--

-- --------------------------------------------------------

--
-- Table structure for table `employee_training_xref`
--


CREATE TABLE IF NOT EXISTS `employee_training_xref` (
    `employee_id` int UNSIGNED NOT NULL,
    `course_id` int UNSIGNED NOT NULL,
    `start_date` varchar(25) NOT NULL,
    `end_date` varchar(25) NOT NULL,
    `status` varchar(25) NOT NULL,
    KEY `course_id_fk_constraint` (`course_id`),
    KEY `employee_id` (`employee_id`,`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    COMMENT='Relates employess to courses taken.';

--
-- RELATIONSHIPS FOR TABLE `employee_training_xref`:
-- `course_id`
-- `courses` -> `id`
-- `employee_id`
-- `employees` -> `id`
--

--
-- Constraints for table `employee_training_xref`
--
ALTER TABLE `employee_training_xref`
    ADD CONSTRAINT `course_id_fk_constraint` FOREIGN KEY (`course_id`)
        REFERENCES `courses` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT `employee_id_fk_constraint` FOREIGN KEY (`employee_id`)
        REFERENCES `employees` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;