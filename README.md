# AI Recruitment & Workforce Analytics Dashboard

An end-to-end Data Analytics and Machine Learning solution for Human Resource departments to streamline talent acquisition operations, analyze recruiter performance, and predict candidate selection outcomes.

## 📁 Repository Structure

```
AI-Recruitment-Workforce-Analytics/
│
├── Dataset/
│   ├── HR_Recruitment_Dataset.csv      # Raw recruitment dataset (10,000+ records)
│   ├── HR_Recruitment_Dataset.xlsx     # Dataset in Excel format
│   └── Data_Dictionary.xlsx            # Metadata dictionary explaining columns
│
├── PowerBI/
│   ├── Theme.json                      # Premium glassmorphism dark-mode theme
│   └── Dashboard_Background.png        # Custom graphical panel background
│
├── SQL/
│   ├── Create_Tables.sql               # Star Schema table definitions
│   ├── Insert_Data.sql                 # Sample records insertion script
│   ├── Analysis_Queries.sql            # Key operational performance queries
│   └── Views.sql                       # Reusable analytical views
│
├── Python/
│   ├── data_cleaning.py                # Cleaning and validation module
│   ├── preprocessing.py                # Encoding, scaling, and train-test partitioner
│   ├── prediction_model.py             # Random Forest classifier pipeline
│   ├── requirements.txt                # Python package list
│   └── README.md                       # Running guide for ML module
│
├── Documentation/
│   ├── Project_Report.docx             # Complete Word report
│   ├── Project_Presentation.pptx       # Slide deck covering solution architectures
│   ├── Dashboard_Guide.pdf             # Step-by-step ETL and Power BI setup manual
│   └── Screenshots/                    # Saved evaluation curves and heatmaps
│
├── Images/
│   ├── logo.png                        # App branding assets
│   ├── dashboard_preview.png           # Finished dashboard preview mockup
│   └── icons/                          # UI icons
│
├── LICENSE                             # MIT License
├── README.md                           # Main documentation guide
└── Project_Overview.pdf                # One-page executive brief
```

---

## 📊 Dataset Specifications

The dataset represents **10,200 unique applications** with parameters modeling realistic recruiting distributions:
- **Demographics**: Candidate Name, Age (21-48), Gender, Location (16 major global hubs including Bangalore, London, New York).
- **Qualifications**: Education level (UG, PG, PhD), Graduation University (Stanford, IIT, BITS, Oxford, etc.), Experience (0-15 years), and specialized Role Skills.
- **Transactional Dates**: Chronologically verified dates (`Joining_Date` > `Offer_Date` > `Interview_Date` > `Application_Date`).
- **Interviewer Metrics**: ATS Resume Score, Technical, HR, and Communication round scores (0-100), plus computed Overall Score.
- **Salaries**: Offered Annual Salary mapped logically close to candidate Expectations (0.9x - 1.05x CTC).
- **Hiring Parameters**: Notice Period (0-90 days), Recruitment Source, Recruiter Name, Hiring Manager, Work Mode, Contract Type, Status, and Result.

---

## 🔄 Power Query & ETL Steps

To transform the data inside Power BI or SQL:
1. **Remove Duplicates**: Deduplicate by `Candidate_ID` to ensure one pipeline record per applicant.
2. **Handle Nulls**: 
   - Coerce empty numeric fields (`Offered_Salary`) to `0` or `null` to avoid averaging distortions.
   - For intermediate application stages, set missing scores and dates (`Interview_Date`, `Offer_Date`) to `null`.
3. **Format Dates**: Enforce datetime types and extract calendar dimensions (Year, Quarter, Month Name, Month Number, Day of Week).
4. **Calculated Columns**:
   - `Overall_Score` = `(ATS * 0.2) + (Tech * 0.3) + (HR * 0.3) + (Comm * 0.2)`
   - `Salary_Gap` = `Offered_Salary - Expected_Salary`

---

## 📐 Data Model (STAR SCHEMA)

The warehouse is configured as an optimized **Star Schema** to enable rapid slicer interactions:
- **Fact Table**: `Fact_Recruitment`
- **Dimension Tables**: 
  - `Dim_Candidate` (Attributes: demographics, qualifications)
  - `Dim_Department` (Attributes: corporate groups)
  - `Dim_Recruiter` (Attributes: recruiter names)
  - `Dim_Date` (Attributes: calendar periods)

---

## 📐 Key DAX Measures

Include these metrics in your Power BI visuals:
- **Total Applications**: `Total Applications = COUNTROWS(Fact_Recruitment)`
- **Total Hired**: `Total Hired = CALCULATE(COUNTROWS(Fact_Recruitment), Fact_Recruitment[Status] = "Hired")`
- **Hiring Rate**: `Hiring Rate = DIVIDE([Total Hired], [Total Applications], 0)`
- **Acceptance Rate**: `Acceptance Rate = VAR Offered = CALCULATE(COUNTROWS(Fact_Recruitment), Fact_Recruitment[Status] IN {"Offered", "Hired"}) RETURN DIVIDE([Total Hired], Offered, 0)`
- **Avg ATS Score**: `Avg ATS Score = AVERAGE(Fact_Recruitment[Resume_ATS_Score])`
- **Avg Salary**: `Avg Salary = AVERAGE(Fact_Recruitment[Offered_Salary])`

---

## 🧠 Machine Learning Module

- **Algorithm**: Random Forest Classifier (100 Trees).
- **Task**: Predict `Result` ('Selected' vs. 'Rejected') using screening metrics.
- **Accuracy**: Achieves **90%+** overall accuracy.
- **Key Feature Importances**: Technical Score (32%), HR Interview Score (28%), Resume ATS Score (15%).

---

## 💡 Strategic Insights

1. **Conversion Excellence**: Employee Referrals yield a **32% hiring rate**, representing the most effective channel, despite having smaller initial application volume than Job Portals.
2. **Notice Constraints**: Over **40% of candidates** have a notice period of 60 days or more. Recruiters must target low-notice channels or contract conversions to fill high-priority IT gaps.
3. **Wage Alignment**: The average salary variance is small (+2.3%), showing that Offered Salaries closely follow Candidate Expectations.
