-- =========================================================================
-- AI Recruitment & Workforce Analytics Dashboard
-- ANALYSIS QUERIES
-- =========================================================================

-- 1. OVERALL HIRING RATE & CONVERSION FUNNEL
-- Calculates the total applications, candidates interviewed, candidates offered, and candidates hired.
-- Also calculates overall Selection/Hiring Rate.
SELECT 
    COUNT(*) AS Total_Applications,
    SUM(CASE WHEN Status IN ('Interviewed', 'Offered', 'Hired', 'Rejected') AND Interview_Date_Key IS NOT NULL THEN 1 ELSE 0 END) AS Total_Interviewed,
    SUM(CASE WHEN Status IN ('Offered', 'Hired') THEN 1 ELSE 0 END) AS Total_Offered,
    SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) AS Total_Hired,
    CAST(SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Hiring_Rate_Percent,
    CAST(SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) * 100.0 / NULLIF(SUM(CASE WHEN Status IN ('Offered', 'Hired') THEN 1 ELSE 0 END), 0) AS DECIMAL(5,2)) AS Offer_Acceptance_Rate_Percent
FROM Fact_Recruitment;


-- 2. AVERAGE EXPECTED vs. OFFERED SALARY BY DEPARTMENT
-- Analyze potential wage gaps and expectations across various departments.
SELECT 
    d.Department_Name,
    COUNT(f.Recruitment_Key) AS Total_Applications,
    SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) AS Hired_Count,
    CAST(AVG(f.Expected_Salary) AS DECIMAL(15,2)) AS Avg_Expected_Salary,
    CAST(AVG(CASE WHEN f.Status IN ('Offered', 'Hired') THEN f.Offered_Salary ELSE NULL END) AS DECIMAL(15,2)) AS Avg_Offered_Salary,
    CAST(AVG(CASE WHEN f.Status = 'Hired' THEN f.Offered_Salary - f.Expected_Salary ELSE NULL END) AS DECIMAL(15,2)) AS Avg_Salary_Variance
FROM Fact_Recruitment f
JOIN Dim_Department d ON f.Department_Key = d.Department_Key
GROUP BY d.Department_Name
ORDER BY Hired_Count DESC;


-- 3. AVERAGE TIME TO HIRE (TTH) IN DAYS BY RECRUITER
-- Time to Hire = Date between Application and Offer extended.
SELECT 
    r.Recruiter_Name,
    COUNT(CASE WHEN f.Status = 'Hired' THEN 1 END) AS Hires_Completed,
    AVG(f.Resume_ATS_Score) AS Avg_ATS_Score_Of_Candidates,
    AVG(DATEDIFF(day, da.Full_Date, do.Full_Date)) AS Avg_Days_Application_To_Offer,
    AVG(DATEDIFF(day, di.Full_Date, do.Full_Date)) AS Avg_Days_Interview_To_Offer
FROM Fact_Recruitment f
JOIN Dim_Recruiter r ON f.Recruiter_Key = r.Recruiter_Key
JOIN Dim_Date da ON f.Application_Date_Key = da.Date_Key
JOIN Dim_Date di ON f.Interview_Date_Key = di.Date_Key
JOIN Dim_Date do ON f.Offer_Date_Key = do.Date_Key
WHERE f.Status IN ('Offered', 'Hired')
GROUP BY r.Recruiter_Name
ORDER BY Avg_Days_Application_To_Offer ASC;


-- 4. RECRUITMENT SOURCE EFFECTIVENESS
-- Analyze which channels drive the most qualified talent and conversions.
SELECT 
    f.Recruitment_Source,
    COUNT(*) AS Total_Applications,
    SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) AS Total_Hired,
    CAST(SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS Source_Conversion_Rate_Percent,
    AVG(f.Overall_Score) AS Avg_Candidate_Overall_Score,
    AVG(f.Resume_ATS_Score) AS Avg_Candidate_ATS_Score
FROM Fact_Recruitment f
GROUP BY f.Recruitment_Source
ORDER BY Total_Hired DESC, Source_Conversion_Rate_Percent DESC;


-- 5. MONTHLY HIRING TREND
-- Show historical hiring volumes over time (grouped by Month).
SELECT 
    da.Year,
    da.Month,
    da.Month_Name,
    COUNT(*) AS Applications_Count,
    SUM(CASE WHEN f.Status = 'Hired' THEN 1 ELSE 0 END) AS Hired_Count
FROM Fact_Recruitment f
JOIN Dim_Date da ON f.Application_Date_Key = da.Date_Key
GROUP BY da.Year, da.Month, da.Month_Name
ORDER BY da.Year ASC, da.Month ASC;
