/* ******************************************************
 Insert test data into the grant_investigator database.
******************************************************* */

-- Switch to the grant_investigator database.
USE `grants_investigators`

-- 1. Insert Test Grants
INSERT INTO `grants` (`grant_name`, `grant_number`, `funding_agency`, `funding_amount`, `start_date`, `end_date`) 
    VALUES ('Quantum Computing for Climate Modeling', 'NSF-2026-QC99', 'National Science Foundation', 1250000.00, '2026-09-01', '2029-08-31');

INSERT INTO `grants` (`grant_name`, `grant_number`, `funding_agency`, `funding_amount`, `start_date`, `end_date`) 
    VALUES ('Deep Learning in Genomic Sequencing', 'NIH-R01-HG102', 'National Institutes of Health', 850000.00, '2026-10-15', '2028-10-14');

INSERT INTO `grants` (`grant_name`, `grant_number`, `funding_agency`, `funding_amount`, `start_date`, `end_date`) 
    VALUES ('Urban Infrastructure Resilience Study', 'DOE-EERE-401', 'Department of Energy', 500000.00, '2027-01-01', '2027-12-31');

-- 2. Insert Test Investigators
INSERT INTO `investigators` (`first_name`, `last_name`, `email`, `institution`) 
    VALUES ('Alan', 'Turing', 'a.turing@university.edu', 'Institute for Advanced Study');

INSERT INTO `investigators` (`first_name`, `last_name`, `email`, `institution`) 
    VALUES ('Grace', 'Hopper', 'g.hopper@navy.mil', 'Yale University');

INSERT INTO `investigators` (`first_name`, `last_name`, `email`, `institution`) 
    VALUES ('Ada', 'Lovelace', 'ada.l@analytical.org', 'University of London');

INSERT INTO `investigators` (`first_name`, `last_name`, `email`, `institution`) 
    VALUES ('Katherine', 'Johnson', 'k.johnson@nasa.gov', 'West Virginia University');

-- 3. Link Grants and Investigators (Cross-Reference Table)
-- (Assuming IDs generated starting from 1 sequentially)

-- Grant 1 (Quantum Climate) has Alan (PI) and Grace (Co-PI)
INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (1, 1, 'Principal Investigator', 40.00);

INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (1, 2, 'Co-Principal Investigator', 25.00);

-- Grant 2 (Genomics) has Ada (PI) and Alan (Co-Investigator)
INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (2, 3, 'Principal Investigator', 50.00);

INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (2, 1, 'Co-Investigator', 20.00);

-- Grant 3 (Infrastructure) has Katherine (PI), Grace (Co-Investigator), and Ada (Co-Investigator)
INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (3, 4, 'Principal Investigator', 60.00);

INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (3, 2, 'Co-Investigator', 15.00);

INSERT INTO `grant_investigator_xref` (`grant_id`, `investigator_id`, `role`, `grant_percent`) 
    VALUES (3, 3, 'Co-Investigator', 15.00);