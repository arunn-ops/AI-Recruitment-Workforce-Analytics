import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(num_records=10000):
    print(f"Starting dataset generation of {num_records} records...")
    
    # Random seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Pre-defined realistic lists
    first_names_indian = ["Aarav", "Aditya", "Amit", "Arjun", "Ananya", "Diya", "Isha", "Kabir", "Neha", "Rahul", 
                          "Rohan", "Siddharth", "Vikram", "Pooja", "Rajesh", "Sunita", "Deepak", "Meera", "Varun", "Riya"]
    last_names_indian = ["Sharma", "Verma", "Gupta", "Mehta", "Patel", "Reddy", "Nair", "Joshi", "Rao", "Kumar", 
                         "Singh", "Choudhury", "Das", "Sen", "Bose", "Pillai", "Iyer", "Mishra", "Pandey", "Chatterjee"]
    
    first_names_global = ["John", "Emily", "Michael", "Sarah", "David", "Jessica", "James", "Emma", "Robert", "Olivia",
                           "William", "Sophia", "Richard", "Isabella", "Joseph", "Mia", "Thomas", "Charlotte", "Charles", "Amelia"]
    last_names_global = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson",
                          "Martinez", "Anderson", "Taylor", "Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "White"]
    
    cities = [
        # Indian cities
        "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune", "Chennai", "Kolkata", "Gurgaon",
        # Global cities
        "London", "New York", "San Francisco", "Singapore", "Berlin", "Toronto", "Sydney", "Dubai"
    ]
    
    universities = [
        "IIT Bombay", "IIT Delhi", "IIT Madras", "BITS Pilani", "Delhi University", "IIM Bangalore", "IIM Ahmedabad",
        "Stanford University", "MIT", "University of California, Berkeley", "University of Oxford", 
        "University of Cambridge", "University of Toronto", "National University of Singapore"
    ]
    
    departments = ["IT & Engineering", "Data Analytics", "HR", "Finance", "Sales & Marketing", "Operations"]
    
    roles_by_dept = {
        "IT & Engineering": ["Python Developer", "Frontend Developer", "Backend Developer", "DevOps Engineer", "QA Engineer", "Full Stack Developer"],
        "Data Analytics": ["Data Analyst", "Data Scientist", "Machine Learning Engineer", "BI Developer", "Data Engineer"],
        "HR": ["HR Recruiter", "HR Manager", "HR Generalist", "Talent Acquisition Specialist"],
        "Finance": ["Financial Analyst", "Accountant", "Finance Manager", "Investment Analyst"],
        "Sales & Marketing": ["Sales Executive", "Marketing Manager", "SEO Specialist", "Business Development Manager"],
        "Operations": ["Operations Associate", "Operations Manager", "Supply Chain Analyst"]
    }
    
    skills_by_role = {
        "Python Developer": ["Python", "Django", "FastAPI", "REST APIs", "SQL", "Git"],
        "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Vue", "TypeScript"],
        "Backend Developer": ["Java", "Spring Boot", "SQL", "Microservices", "REST APIs", "AWS"],
        "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform", "Linux"],
        "QA Engineer": ["Selenium", "Java", "Python", "Manual Testing", "Jira", "SQL"],
        "Full Stack Developer": ["React", "Node.js", "Express", "MongoDB", "JavaScript", "SQL", "Git"],
        "Data Analyst": ["Python", "SQL", "Power BI", "Excel", "Tableau", "Statistics"],
        "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics", "R", "NLP", "Pandas"],
        "Machine Learning Engineer": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "SQL", "MLOps"],
        "BI Developer": ["Power BI", "DAX", "SQL", "Tableau", "ETL", "Data Modeling"],
        "Data Engineer": ["Python", "SQL", "Spark", "Hadoop", "ETL", "Airflow", "AWS"],
        "HR Recruiter": ["Sourcing", "Interviewing", "Communication", "Applicant Tracking Systems", "Negotiation"],
        "HR Manager": ["Employee Relations", "Performance Management", "HR Strategy", "Compliance", "Leadership"],
        "HR Generalist": ["Onboarding", "Payroll", "HR Administration", "Employee Engagement", "Excel"],
        "Talent Acquisition Specialist": ["Employer Branding", "Talent Pipelines", "Sourcing", "Applicant Tracking Systems", "Communication"],
        "Financial Analyst": ["Excel", "Financial Modeling", "SQL", "Corporate Finance", "Valuation"],
        "Accountant": ["Accounting Principles", "Taxation", "Tally", "Excel", "Auditing"],
        "Finance Manager": ["Financial Planning", "Budgeting", "Risk Management", "Leadership", "Excel"],
        "Investment Analyst": ["Market Research", "Financial Modeling", "Portfolio Management", "Excel", "SQL"],
        "Sales Executive": ["Sales", "Communication", "Negotiation", "CRM", "Lead Generation"],
        "Marketing Manager": ["Digital Marketing", "Brand Strategy", "Content Marketing", "Google Analytics", "Social Media"],
        "SEO Specialist": ["SEO", "Google Analytics", "Keyword Research", "HTML", "Link Building"],
        "Business Development Manager": ["B2B Sales", "Client Relations", "Strategy", "Negotiation", "CRM"],
        "Operations Associate": ["Process Management", "Excel", "Logistics", "Problem Solving", "Communication"],
        "Operations Manager": ["Operations Management", "Process Improvement", "Supply Chain", "Budgeting", "Leadership"],
        "Supply Chain Analyst": ["Supply Chain", "Logistics", "Excel", "SQL", "Inventory Management"]
    }
    
    recruitment_sources = ["LinkedIn", "Indeed", "Naukri.com", "Employee Referral", "Company Website", "Campus Placement", "Agency"]
    recruiters = ["Vikram Malhotra", "Sarah Jenkins", "Neha Sharma", "Rohan Verma", "Emily Smith", "David Miller"]
    hiring_managers = ["Arjun Mehta", "Michael Davis", "Ananya Reddy", "Robert Jones", "Siddharth Sen", "Sophia Taylor"]
    
    statuses = ["Applied", "Interviewed", "Offered", "Hired", "Rejected"]
    work_modes = ["Remote", "Hybrid", "Onsite"]
    employment_types = ["Full-time", "Intern", "Contract"]
    
    data = []
    
    # Let's generate records
    for i in range(1, num_records + 1):
        candidate_id = f"CAN_{20260000 + i}"
        
        # Indian/Global candidate split (60% Indian, 40% Global)
        is_indian = random.random() < 0.6
        if is_indian:
            first_name = random.choice(first_names_indian)
            last_name = random.choice(last_names_indian)
        else:
            first_name = random.choice(first_names_global)
            last_name = random.choice(last_names_global)
        
        candidate_name = f"{first_name} {last_name}"
        
        # Demographics
        age = random.randint(21, 48)
        gender_rand = random.random()
        if gender_rand < 0.48:
            gender = "Male"
        elif gender_rand < 0.96:
            gender = "Female"
        else:
            gender = "Other"
            
        location = random.choice(cities)
        
        education_rand = random.random()
        if education_rand < 0.60:
            education = "UG"  # Undergrad
        elif education_rand < 0.92:
            education = "PG"  # Postgrad
        else:
            education = "PhD"
            
        university = random.choice(universities)
        
        # Experience: logical relationship to age
        # Age 21: max exp 0-1 years. Age 30: max exp 8-9 years.
        max_exp = max(0, age - 21)
        experience = random.randint(0, min(15, max_exp))
        
        # Role & Department
        department = random.choice(departments)
        job_role = random.choice(roles_by_dept[department])
        
        # Skills (pick 3 to 5 matching skills, and maybe 1 generic skill)
        role_skills = skills_by_role[job_role]
        num_skills = random.randint(3, 5)
        picked_skills = random.sample(role_skills, min(num_skills, len(role_skills)))
        
        generic_skills = ["Communication", "Teamwork", "Problem Solving", "Agile", "Excel", "SQL"]
        if random.random() < 0.4:
            picked_skills.append(random.choice(generic_skills))
            
        # Deduplicate skills list
        picked_skills = list(set(picked_skills))
        skills_str = ", ".join(picked_skills)
        
        # Recruitment source
        recruitment_source = random.choice(recruitment_sources)
        
        # Scores (0-100)
        # Note: we want scores to correlate with experience and education slightly
        score_boost = min(15, experience * 1.2) + (5 if education == "PG" else 10 if education == "PhD" else 0)
        
        resume_score = min(100, int(np.random.normal(65, 12) + score_boost * 0.5))
        technical_score = min(100, int(np.random.normal(60, 15) + score_boost * 0.8))
        hr_score = min(100, int(np.random.normal(70, 10) + score_boost * 0.3))
        comm_score = min(100, int(np.random.normal(68, 12) + score_boost * 0.4))
        
        # Ensure scores are at least 0
        resume_score = max(0, resume_score)
        technical_score = max(0, technical_score)
        hr_score = max(0, hr_score)
        comm_score = max(0, comm_score)
        
        # Overall score calculated
        overall_score = round(
            (resume_score * 0.20) + 
            (technical_score * 0.30) + 
            (hr_score * 0.30) + 
            (comm_score * 0.20), 2
        )
        
        # Notice period
        notice_period = random.choice([0, 15, 30, 45, 60, 90])
        
        # Salaries (Expected Salary depends on experience and department)
        # Baseline salaries based on department and experience
        dept_multipliers = {
            "IT & Engineering": 1.5,
            "Data Analytics": 1.6,
            "HR": 1.0,
            "Finance": 1.2,
            "Sales & Marketing": 1.1,
            "Operations": 0.95
        }
        
        base_expected = 400000 + (experience * 80000)
        expected_salary = int(base_expected * dept_multipliers[department] * random.uniform(0.9, 1.1))
        # Round to nearest 10,000
        expected_salary = (expected_salary // 10000) * 10000
        
        # Status & Result Logic
        # Higher overall score + experience -> higher chance of selection
        # Status can be Applied, Interviewed, Offered, Hired, Rejected
        # We will determine the status based on overall score
        status_rand = random.random()
        
        # Let's map final results:
        # If overall score >= 75: High chance of Offered / Hired
        # If overall score between 60 and 75: Medium chance
        # If overall score < 60: Low chance (mostly rejected or interviewed and rejected)
        
        if overall_score >= 76:
            if status_rand < 0.65:
                status = "Hired"
                result = "Selected"
            elif status_rand < 0.90:
                status = "Offered"
                result = "Selected"
            elif status_rand < 0.97:
                status = "Interviewed"
                result = "Selected" # Selected but declined/still interviewing
            else:
                status = "Rejected"
                result = "Rejected"
        elif overall_score >= 62:
            if status_rand < 0.25:
                status = "Hired"
                result = "Selected"
            elif status_rand < 0.45:
                status = "Offered"
                result = "Selected"
            elif status_rand < 0.75:
                status = "Interviewed"
                result = "Rejected" # Made it to interview, but rejected
            elif status_rand < 0.95:
                status = "Rejected"
                result = "Rejected"
            else:
                status = "Applied"
                result = "Rejected"
        else: # Low score
            if status_rand < 0.85:
                status = "Rejected"
                result = "Rejected"
            elif status_rand < 0.95:
                status = "Interviewed"
                result = "Rejected"
            else:
                status = "Applied"
                result = "Rejected"
        
        # Job_Role / department correction (for non-hired statuses we can keep Applied)
        if overall_score < 45 and status != "Applied":
            status = "Rejected"
            result = "Rejected"
            
        # Date generation: logical order
        # We'll place application date in 2025 or 2026
        # Application date
        days_ago = random.randint(10, 360) # within the last year
        app_date = datetime(2026, 7, 12) - timedelta(days=days_ago)
        
        interview_date = None
        offer_date = None
        joining_date = None
        offered_salary = 0
        
        if status in ["Interviewed", "Offered", "Hired", "Rejected"] and overall_score >= 45:
            # Took 5 to 20 days to schedule interview
            int_days = random.randint(5, 20)
            interview_date = app_date + timedelta(days=int_days)
            
            if status in ["Offered", "Hired"] or (status == "Rejected" and random.random() < 0.4 and overall_score > 60):
                # Took 3 to 10 days for decision/offer
                off_days = random.randint(3, 10)
                offer_date = interview_date + timedelta(days=off_days)
                
                # Offered salary is close to expected (e.g., 0.92x to 1.05x expected)
                offered_salary = int(expected_salary * random.uniform(0.92, 1.05))
                offered_salary = (offered_salary // 10000) * 10000
                
                if status == "Hired":
                    # Joining date depends on notice period
                    joining_date = offer_date + timedelta(days=notice_period + random.randint(1, 10))
            
        # Recruiter & Hiring manager assignments
        recruiter = random.choice(recruiters)
        hiring_manager = random.choice(hiring_managers)
        
        work_mode = random.choice(work_modes)
        employment_type = random.choice(employment_types)
        
        # Prepare date strings (YYYY-MM-DD or empty)
        app_date_str = app_date.strftime('%Y-%m-%d')
        int_date_str = interview_date.strftime('%Y-%m-%d') if interview_date else ""
        off_date_str = offer_date.strftime('%Y-%m-%d') if offer_date else ""
        join_date_str = joining_date.strftime('%Y-%m-%d') if joining_date else ""
        
        record = {
            "Candidate_ID": candidate_id,
            "Candidate_Name": candidate_name,
            "Age": age,
            "Gender": gender,
            "Location": location,
            "Education": education,
            "University": university,
            "Experience": experience,
            "Skills": skills_str,
            "Job_Role": job_role,
            "Department": department,
            "Application_Date": app_date_str,
            "Interview_Date": int_date_str,
            "Offer_Date": off_date_str,
            "Joining_Date": join_date_str,
            "Recruitment_Source": recruitment_source,
            "Resume_ATS_Score": resume_score,
            "Technical_Score": technical_score,
            "HR_Score": hr_score,
            "Communication_Score": comm_score,
            "Overall_Score": overall_score,
            "Expected_Salary": expected_salary,
            "Offered_Salary": offered_salary if offered_salary > 0 else "",
            "Notice_Period": notice_period,
            "Status": status,
            "Recruiter_Name": recruiter,
            "Hiring_Manager": hiring_manager,
            "Work_Mode": work_mode,
            "Employment_Type": employment_type,
            "Result": result
        }
        
        data.append(record)
        
    df = pd.DataFrame(data)
    
    # Save folder path checks
    output_dir = r"C:\Users\Surya\.gemini\antigravity\scratch\AI-Recruitment-Workforce-Analytics\Dataset"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "HR_Recruitment_Dataset.csv")
    xlsx_path = os.path.join(output_dir, "HR_Recruitment_Dataset.xlsx")
    
    # Save CSV
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully saved to CSV: {csv_path}")
    
    # Save Excel (note: write empty values correctly for Offered_Salary / Dates)
    # Convert Offered_Salary back to numeric for Excel, replacing empty strings with NaN
    df_excel = df.copy()
    df_excel['Offered_Salary'] = pd.to_numeric(df_excel['Offered_Salary'], errors='coerce')
    
    # Format date columns in excel
    for col in ["Application_Date", "Interview_Date", "Offer_Date", "Joining_Date"]:
        df_excel[col] = pd.to_datetime(df_excel[col], errors='coerce')
        # Excel handles datetime objects natively
        
    df_excel.to_excel(xlsx_path, index=False, sheet_name="Recruitment_Data")
    print(f"Dataset successfully saved to Excel: {xlsx_path}")
    
    # Create Data Dictionary Excel
    dict_data = [
        {"Column Name": "Candidate_ID", "Data Type": "Varchar (Text)", "Description": "Unique identifier for each candidate"},
        {"Column Name": "Candidate_Name", "Data Type": "Varchar (Text)", "Description": "Full name of the candidate"},
        {"Column Name": "Age", "Data Type": "Integer", "Description": "Age of the candidate (ranging 18-50)"},
        {"Column Name": "Gender", "Data Type": "Varchar (Text)", "Description": "Candidate gender (Male, Female, Other)"},
        {"Column Name": "Location", "Data Type": "Varchar (Text)", "Description": "Major Indian and global tech hub locations"},
        {"Column Name": "Education", "Data Type": "Varchar (Text)", "Description": "Highest qualification degree (UG, PG, PhD)"},
        {"Column Name": "University", "Data Type": "Varchar (Text)", "Description": "Name of the university graduated from"},
        {"Column Name": "Experience", "Data Type": "Integer", "Description": "Years of professional work experience (0-15 years)"},
        {"Column Name": "Skills", "Data Type": "Varchar (Text)", "Description": "Comma-separated core tech/domain skills"},
        {"Column Name": "Job_Role", "Data Type": "Varchar (Text)", "Description": "Job profile applied for"},
        {"Column Name": "Department", "Data Type": "Varchar (Text)", "Description": "Department the role belongs to (e.g. IT, HR, Finance, etc.)"},
        {"Column Name": "Application_Date", "Data Type": "Date", "Description": "Date when candidate applied (YYYY-MM-DD)"},
        {"Column Name": "Interview_Date", "Data Type": "Date", "Description": "Date when interview was conducted (YYYY-MM-DD)"},
        {"Column Name": "Offer_Date", "Data Type": "Date", "Description": "Date when offer letter was extended (YYYY-MM-DD)"},
        {"Column Name": "Joining_Date", "Data Type": "Date", "Description": "Date when the candidate joined the company (YYYY-MM-DD)"},
        {"Column Name": "Recruitment_Source", "Data Type": "Varchar (Text)", "Description": "Channel through which candidate applied (e.g. LinkedIn, Referral)"},
        {"Column Name": "Resume_ATS_Score", "Data Type": "Integer (0-100)", "Description": "Automated Applicant Tracking System score for resume alignment"},
        {"Column Name": "Technical_Score", "Data Type": "Integer (0-100)", "Description": "Score achieved in technical evaluation round"},
        {"Column Name": "HR_Score", "Data Type": "Integer (0-100)", "Description": "Score achieved in behavioral/HR round"},
        {"Column Name": "Communication_Score", "Data Type": "Integer (0-100)", "Description": "Score in communication and soft skills assessment"},
        {"Column Name": "Overall_Score", "Data Type": "Float (0-100)", "Description": "Weighted average score: 20% ATS, 30% Tech, 30% HR, 20% Comm"},
        {"Column Name": "Expected_Salary", "Data Type": "Decimal/Integer", "Description": "Annual CTC salary expected by candidate (INR/Equivalent)"},
        {"Column Name": "Offered_Salary", "Data Type": "Decimal/Integer", "Description": "Annual CTC salary offered by the company (only for Offered/Hired)"},
        {"Column Name": "Notice_Period", "Data Type": "Integer (Days)", "Description": "Candidate's current company notice period in days (0, 15, 30, 45, 60, 90)"},
        {"Column Name": "Status", "Data Type": "Varchar (Text)", "Description": "Current application recruitment state (Applied, Interviewed, Offered, Hired, Rejected)"},
        {"Column Name": "Recruiter_Name", "Data Type": "Varchar (Text)", "Description": "Name of the recruiter handling the candidate"},
        {"Column Name": "Hiring_Manager", "Data Type": "Varchar (Text)", "Description": "Name of the prospective manager"},
        {"Column Name": "Work_Mode", "Data Type": "Varchar (Text)", "Description": "Mode of work (Remote, Hybrid, Onsite)"},
        {"Column Name": "Employment_Type", "Data Type": "Varchar (Text)", "Description": "Type of contract (Full-time, Intern, Contract)"},
        {"Column Name": "Result", "Data Type": "Varchar (Text)", "Description": "Final outcome of the recruitment cycle (Selected, Rejected)"}
    ]
    
    dict_df = pd.DataFrame(dict_data)
    dict_path = os.path.join(output_dir, "Data_Dictionary.xlsx")
    dict_df.to_excel(dict_path, index=False, sheet_name="Data Dictionary")
    print(f"Data Dictionary saved to: {dict_path}")
    print("Dataset generation complete!")

if __name__ == "__main__":
    generate_data(10200) # Slightly more than 10,000 as requested
