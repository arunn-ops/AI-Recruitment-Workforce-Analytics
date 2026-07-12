-- =========================================================================
-- AI Recruitment & Workforce Analytics Dashboard
-- REUSABLE DATABASE VIEWS
-- =========================================================================

-- 1. View: Hiring Summary (Fact Table joined with Candidate, Dept, and Application Date Dimensions)
-- Provides a clean, denormalized view for direct reporting or simple query connections.
CREATE VIEW v_Hiring_Summary AS
SELECT 
    f.Recruitment_Key,
    c.Candidate_ID,
    c.Candidate_Name,
    c.Age,
    c.Gender,
    c.Location AS Candidate_Location,
    c.Education,
    c.University,
    c.Skills,
    f.Job_Role,
    d.Department_Name,
    da.Full_Date AS Application_Date,
    di.Full_Date AS Interview_Date,
    do.Full_Date AS Offer_Date,
    dj.Full_Date AS Joining_Date,
    f.Recruitment_Source,
    f.Resume_ATS_Score,
    f.Technical_Score,
    f.HR_Score,
    f.Communication_Score,
    f.Overall_Score,
    f.Expected_Salary,
    f.Offered_Salary,
    f.Notice_Period,
    f.Status,
    r.Recruiter_Name,
    f.Hiring_Manager,
    f.Work_Mode,
    f.Employment_Type,
    f.Result
FROM Fact_Recruitment f
JOIN Dim_Candidate c ON f.Candidate_Key = c.Candidate_Key
JOIN Dim_Department d ON f.Department_Key = d.Department_Key
JOIN Dim_Recruiter r ON f.Recruiter_Key = r.Recruiter_Key
JOIN Dim_Date da ON f.Application_Date_Key = da.Date_Key
LEFT JOIN Dim_Date di ON f.Interview_Date_Key = di.Date_Key
LEFT JOIN Dim_Date do ON f.Offer_Date_Key = do.Date_Key
LEFT JOIN Dim_Date dj ON f.Joining_Date_Key = dj.Date_Key;


-- 2. View: Recruiter Performance
-- Aggregates metrics for recruiters, including their hire volumes, average ATS scores and hire rates.
CREATE VIEW v_Recruiter_Performance AS
SELECT 
    r.Recruiter_Name,
    COUNT(f.Recruitment_Key) AS Total_Applications_Managed,
    SUM(CASE WHEN f.Status = 'Interviewed' THEN 1 ELSE 0 END) AS Total_Interviewed,
    SUM(CASE WHEN f.Status = 'Offered' THEN 1 ELSE 0 END) AS Total_Offered,
    SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) AS Total_Hired,
    CAST(SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) * 100.0 / COUNT(f.Recruitment_Key) AS DECIMAL(5,2)) AS Recruiter_Hiring_Rate_Percent,
    AVG(f.Overall_Score) AS Avg_Overall_Score_Of_Candidates
FROM Fact_Recruitment f
JOIN Dim_Recruiter r ON f.Recruiter_Key = r.Recruiter_Key
GROUP BY r.Recruiter_Name;


-- 3. View: Department Recruitment Metrics
-- Aggregates metrics for departments, showing hiring stats, average age and average notice periods.
CREATE VIEW v_Department_Recruitment_Metrics AS
SELECT 
    d.Department_Name,
    COUNT(f.Recruitment_Key) AS Total_Applications,
    SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) AS Hired_Count,
    CAST(SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) * 100.0 / COUNT(f.Recruitment_Key) AS DECIMAL(5,2)) AS Dept_Hiring_Rate_Percent,
    AVG(c.Age) AS Avg_Candidate_Age,
    AVG(f.Notice_Period) AS Avg_Notice_Period_Days
FROM Fact_Recruitment f
JOIN Dim_Department d ON f.Department_Key = d.Department_Key
JOIN Dim_Candidate c ON f.Candidate_Key = c.Candidate_Key
GROUP BY d.Department_Name;
