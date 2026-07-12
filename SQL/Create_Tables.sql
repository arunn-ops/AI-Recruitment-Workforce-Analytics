-- =========================================================================
-- AI Recruitment & Workforce Analytics Dashboard
-- CREATE TABLES SCRIPT (STAR SCHEMA)
-- Compatible with SQL Server, PostgreSQL, or standard ANSI SQL.
-- =========================================================================

-- Create Dimension: Department
CREATE TABLE Dim_Department (
    Department_Key INT IDENTITY(1,1) PRIMARY KEY,
    Department_Name VARCHAR(50) NOT NULL UNIQUE
);

-- Create Dimension: Recruiter
CREATE TABLE Dim_Recruiter (
    Recruiter_Key INT IDENTITY(1,1) PRIMARY KEY,
    Recruiter_Name VARCHAR(100) NOT NULL UNIQUE
);

-- Create Dimension: Candidate
CREATE TABLE Dim_Candidate (
    Candidate_Key INT IDENTITY(1,1) PRIMARY KEY,
    Candidate_ID VARCHAR(20) NOT NULL UNIQUE,
    Candidate_Name VARCHAR(100) NOT NULL,
    Age INT CHECK (Age BETWEEN 18 AND 60),
    Gender VARCHAR(20) NOT NULL,
    Location VARCHAR(50) NOT NULL,
    Education VARCHAR(20) NOT NULL,
    University VARCHAR(100) NOT NULL,
    Skills VARCHAR(500) NOT NULL
);

-- Create Dimension: Date
CREATE TABLE Dim_Date (
    Date_Key INT PRIMARY KEY, -- Formatted as YYYYMMDD
    Full_Date DATE NOT NULL UNIQUE,
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    Month INT NOT NULL,
    Month_Name VARCHAR(20) NOT NULL,
    Day_Of_Week VARCHAR(20) NOT NULL
);

-- Create Fact Table: Recruitment Fact
CREATE TABLE Fact_Recruitment (
    Recruitment_Key INT IDENTITY(1,1) PRIMARY KEY,
    Candidate_Key INT NOT NULL FOREIGN KEY REFERENCES Dim_Candidate(Candidate_Key),
    Department_Key INT NOT NULL FOREIGN KEY REFERENCES Dim_Department(Department_Key),
    Recruiter_Key INT NOT NULL FOREIGN KEY REFERENCES Dim_Recruiter(Recruiter_Key),
    Application_Date_Key INT NOT NULL FOREIGN KEY REFERENCES Dim_Date(Date_Key),
    Interview_Date_Key INT NULL FOREIGN KEY REFERENCES Dim_Date(Date_Key),
    Offer_Date_Key INT NULL FOREIGN KEY REFERENCES Dim_Date(Date_Key),
    Joining_Date_Key INT NULL FOREIGN KEY REFERENCES Dim_Date(Date_Key),
    Job_Role VARCHAR(100) NOT NULL,
    Recruitment_Source VARCHAR(50) NOT NULL,
    Resume_ATS_Score INT CHECK (Resume_ATS_Score BETWEEN 0 AND 100),
    Technical_Score INT CHECK (Technical_Score BETWEEN 0 AND 100),
    HR_Score INT CHECK (HR_Score BETWEEN 0 AND 100),
    Communication_Score INT CHECK (Communication_Score BETWEEN 0 AND 100),
    Overall_Score DECIMAL(5,2) CHECK (Overall_Score BETWEEN 0.00 AND 100.00),
    Expected_Salary DECIMAL(15,2) NOT NULL,
    Offered_Salary DECIMAL(15,2) NULL,
    Notice_Period INT NOT NULL,
    Status VARCHAR(50) NOT NULL, -- Applied, Interviewed, Offered, Hired, Rejected
    Hiring_Manager VARCHAR(100) NOT NULL,
    Work_Mode VARCHAR(50) NOT NULL, -- Remote, Hybrid, Onsite
    Employment_Type VARCHAR(50) NOT NULL, -- Full-time, Intern, Contract
    Result VARCHAR(50) NOT NULL -- Selected, Rejected
);
