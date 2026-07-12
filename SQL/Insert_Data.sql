-- =========================================================================
-- AI Recruitment & Workforce Analytics Dashboard
-- INSERT DATA SCRIPT (SAMPLE RECORDS)
-- =========================================================================

-- 1. Insert sample departments
INSERT INTO Dim_Department (Department_Name) VALUES 
('IT & Engineering'),
('Data Analytics'),
('HR'),
('Finance'),
('Sales & Marketing'),
('Operations');

-- 2. Insert sample recruiters
INSERT INTO Dim_Recruiter (Recruiter_Name) VALUES 
('Vikram Malhotra'),
('Sarah Jenkins'),
('Neha Sharma'),
('Rohan Verma'),
('Emily Smith'),
('David Miller');

-- 3. Insert sample candidates
INSERT INTO Dim_Candidate (Candidate_ID, Candidate_Name, Age, Gender, Location, Education, University, Skills) VALUES 
('CAN_20260001', 'Aarav Sharma', 28, 'Male', 'Bangalore', 'UG', 'IIT Bombay', 'Python, Django, SQL, Git, Communication'),
('CAN_20260002', 'Neha Reddy', 25, 'Female', 'Hyderabad', 'PG', 'BITS Pilani', 'Power BI, DAX, SQL, Excel, Statistics'),
('CAN_20260003', 'John Smith', 32, 'Male', 'London', 'PG', 'Stanford University', 'Python, Machine Learning, Statistics, NLP, SQL'),
('CAN_20260004', 'Emily Davis', 24, 'Female', 'New York', 'UG', 'MIT', 'HTML, CSS, JavaScript, React, Git'),
('CAN_20260005', 'Varun Nair', 29, 'Male', 'Pune', 'PhD', 'University of Oxford', 'Python, PyTorch, Deep Learning, SQL, Statistics'),
('CAN_20260006', 'Riya Sen', 22, 'Female', 'Kolkata', 'UG', 'Delhi University', 'Sourcing, Communication, Applicant Tracking Systems'),
('CAN_20260007', 'Sarah Jenkins', 35, 'Female', 'San Francisco', 'PG', 'UC Berkeley', 'Employee Relations, HR Strategy, Leadership'),
('CAN_20260008', 'Michael Smith', 30, 'Male', 'Toronto', 'PG', 'University of Toronto', 'Excel, Financial Modeling, Corporate Finance, Valuation'),
('CAN_20260009', 'Ananya Gupta', 27, 'Female', 'Mumbai', 'UG', 'BITS Pilani', 'Sales, Communication, Negotiation, CRM'),
('CAN_20260010', 'Rahul Bose', 34, 'Male', 'Delhi', 'PG', 'IIM Bangalore', 'Operations Management, Process Improvement, Supply Chain');

-- 4. Insert Date Dimension rows for the sample dates
INSERT INTO Dim_Date (Date_Key, Full_Date, Year, Quarter, Month, Month_Name, Day_Of_Week) VALUES 
(20260110, '2026-01-10', 2026, 1, 1, 'January', 'Saturday'),
(20260115, '2026-01-15', 2026, 1, 1, 'January', 'Thursday'),
(20260120, '2026-01-20', 2026, 1, 1, 'January', 'Tuesday'),
(20260125, '2026-01-25', 2026, 1, 1, 'January', 'Sunday'),
(20260130, '2026-01-30', 2026, 1, 1, 'January', 'Friday'),
(20260205, '2026-02-05', 2026, 1, 2, 'February', 'Thursday'),
(20260210, '2026-02-10', 2026, 1, 2, 'February', 'Tuesday'),
(20260215, '2026-02-15', 2026, 1, 2, 'February', 'Sunday'),
(20260220, '2026-02-20', 2026, 1, 2, 'February', 'Friday'),
(20260225, '2026-02-25', 2026, 1, 2, 'February', 'Wednesday'),
(20260301, '2026-03-01', 2026, 1, 3, 'March', 'Sunday'),
(20260305, '2026-03-05', 2026, 1, 3, 'March', 'Thursday'),
(20260310, '2026-03-10', 2026, 1, 3, 'March', 'Tuesday'),
(20260315, '2026-03-15', 2026, 1, 3, 'March', 'Sunday'),
(20260320, '2026-03-20', 2026, 1, 3, 'March', 'Friday'),
(20260325, '2026-03-25', 2026, 1, 3, 'March', 'Wednesday'),
(20260401, '2026-04-01', 2026, 2, 4, 'April', 'Wednesday'),
(20260405, '2026-04-05', 2026, 2, 4, 'April', 'Sunday'),
(20260410, '2026-04-10', 2026, 2, 4, 'April', 'Friday'),
(20260415, '2026-04-15', 2026, 2, 4, 'April', 'Wednesday'),
(20260420, '2026-04-20', 2026, 2, 4, 'April', 'Monday'),
(20260425, '2026-04-25', 2026, 2, 4, 'April', 'Saturday');

-- 5. Insert sample recruitment facts
INSERT INTO Fact_Recruitment (
    Candidate_Key, Department_Key, Recruiter_Key, 
    Application_Date_Key, Interview_Date_Key, Offer_Date_Key, Joining_Date_Key, 
    Job_Role, Recruitment_Source, Resume_ATS_Score, Technical_Score, HR_Score, Communication_Score, Overall_Score,
    Expected_Salary, Offered_Salary, Notice_Period, Status, Hiring_Manager, Work_Mode, Employment_Type, Result
) VALUES 
-- Candidate 1: Hired (IT & Engineering)
(1, 1, 1, 20260110, 20260120, 20260125, 20260301, 'Python Developer', 'LinkedIn', 85, 90, 80, 85, 86.50, 800000.00, 820000.00, 30, 'Hired', 'Arjun Mehta', 'Remote', 'Full-time', 'Selected'),

-- Candidate 2: Hired (Data Analytics)
(2, 2, 3, 20260115, 20260125, 20260130, 20260301, 'BI Developer', 'Employee Referral', 78, 82, 85, 88, 82.70, 700000.00, 720000.00, 30, 'Hired', 'Ananya Reddy', 'Hybrid', 'Full-time', 'Selected'),

-- Candidate 3: Offered (Data Analytics - Selected but not yet joined/joined date null)
(3, 2, 2, 20260205, 20260215, 20260220, NULL, 'Data Scientist', 'LinkedIn', 92, 88, 75, 80, 82.90, 1500000.00, 1600000.00, 60, 'Offered', 'Michael Davis', 'Remote', 'Full-time', 'Selected'),

-- Candidate 4: Rejected (IT & Engineering)
(4, 1, 4, 20260210, 20260220, NULL, NULL, 'Frontend Developer', 'Indeed', 60, 50, 70, 65, 59.50, 600000.00, NULL, 30, 'Rejected', 'Arjun Mehta', 'Onsite', 'Full-time', 'Rejected'),

-- Candidate 5: Hired (Data Analytics)
(5, 2, 1, 20260225, 20260305, 20260310, 20260415, 'Machine Learning Engineer', 'Campus Placement', 88, 95, 90, 92, 91.90, 1200000.00, 1250000.00, 30, 'Hired', 'Ananya Reddy', 'Remote', 'Full-time', 'Selected'),

-- Candidate 6: Rejected (HR)
(6, 3, 3, 20260301, 20260310, NULL, NULL, 'HR Recruiter', 'Naukri.com', 55, 45, 60, 70, 56.50, 400000.00, NULL, 15, 'Rejected', 'Sophia Taylor', 'Hybrid', 'Contract', 'Rejected'),

-- Candidate 7: Hired (HR)
(7, 3, 5, 20260305, 20260315, 20260320, 20260420, 'HR Manager', 'Agency', 82, 80, 88, 90, 84.40, 900000.00, 950000.00, 30, 'Hired', 'Sophia Taylor', 'Onsite', 'Full-time', 'Selected'),

-- Candidate 8: Offered (Finance)
(8, 4, 6, 20260310, 20260320, 20260325, NULL, 'Financial Analyst', 'Company Website', 80, 82, 85, 78, 81.20, 650000.00, 650000.00, 45, 'Offered', 'Robert Jones', 'Hybrid', 'Full-time', 'Selected'),

-- Candidate 9: Applied (Sales & Marketing - In Progress)
(9, 5, 2, 20260401, NULL, NULL, NULL, 'Sales Executive', 'LinkedIn', 70, NULL, NULL, NULL, 14.00, 500000.00, NULL, 0, 'Applied', 'Siddharth Sen', 'Onsite', 'Intern', 'Rejected'),

-- Candidate 10: Hired (Operations)
(10, 6, 4, 20260405, 20260415, 20260420, 20260425, 'Operations Manager', 'Indeed', 75, 70, 82, 85, 77.10, 800000.00, 800000.00, 0, 'Hired', 'Robert Jones', 'Hybrid', 'Full-time', 'Selected');
