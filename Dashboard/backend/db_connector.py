import os
import sqlite3
import pandas as pd
from decimal import Decimal

try:
    import pyodbc
    PYODBC_AVAILABLE = True
except ImportError:
    PYODBC_AVAILABLE = False

# Path to workspace dataset as fallback
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "Dataset", "HR_Recruitment_Dataset_Cleaned.csv")

class DatabaseConnector:
    def __init__(self):
        self.connection_type = None
        self.sql_conn = None
        self.sqlite_conn = None
        self._initialize_connection()

    def _initialize_connection(self):
        """Attempts to connect to MSSQL RecruitmentAnalytics database, falls back to SQLite CSV engine."""
        if PYODBC_AVAILABLE:
            drivers = pyodbc.drivers()
            sql_driver = None
            for d in ['ODBC Driver 17 for SQL Server', 'ODBC Driver 18 for SQL Server', 'SQL Server']:
                if d in drivers:
                    sql_driver = d
                    break
            
            if sql_driver:
                servers = [r'.\SQLEXPRESS', 'localhost', '127.0.0.1', '(local)']
                for server in servers:
                    try:
                        conn_str = f"DRIVER={{{sql_driver}}};SERVER={server};DATABASE=RecruitmentAnalytics;Trusted_Connection=yes;TrustServerCertificate=yes;"
                        conn = pyodbc.connect(conn_str, timeout=3)
                        # Verify view exists
                        cursor = conn.cursor()
                        cursor.execute("SELECT TOP 1 * FROM dbo.v_Hiring_Summary")
                        cursor.fetchone()
                        
                        self.sql_conn = conn
                        self.connection_type = f"SQL Server ({server} - RecruitmentAnalytics)"
                        print(f"Successfully connected to MSSQL: {self.connection_type}")
                        return
                    except Exception as e:
                        continue

        # Fallback to SQLite in-memory engine with exact SQL views
        print("Initializing SQLite fallback engine from clean dataset...")
        self._setup_sqlite_engine()

    def _setup_sqlite_engine(self):
        if not os.path.exists(CSV_PATH):
            raise FileNotFoundError(f"Dataset not found at {CSV_PATH}")

        df = pd.read_csv(CSV_PATH)
        self.sqlite_conn = sqlite3.connect(":memory:", check_same_thread=False)
        df.to_sql("Fact_Recruitment_CSV", self.sqlite_conn, index=False, if_exists="replace")
        
        cursor = self.sqlite_conn.cursor()
        
        # Create SQLite View matching v_Hiring_Summary
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS v_Hiring_Summary AS
            SELECT 
                Candidate_ID, Candidate_Name, Age, Gender, Location AS Candidate_Location,
                Education, University, Skills, Job_Role, Department AS Department_Name,
                Application_Date, Interview_Date, Offer_Date, Joining_Date,
                Recruitment_Source, Resume_ATS_Score, Technical_Score, HR_Score,
                Communication_Score, Overall_Score, Expected_Salary, Offered_Salary,
                Notice_Period, Status, Recruiter_Name, Hiring_Manager, Work_Mode,
                Employment_Type, Result
            FROM Fact_Recruitment_CSV;
        """)

        # Create SQLite View matching v_Recruiter_Performance
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS v_Recruiter_Performance AS
            SELECT 
                Recruiter_Name,
                COUNT(*) AS Total_Applications_Managed,
                SUM(CASE WHEN Status = 'Interviewed' THEN 1 ELSE 0 END) AS Total_Interviewed,
                SUM(CASE WHEN Status = 'Offered' THEN 1 ELSE 0 END) AS Total_Offered,
                SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) AS Total_Hired,
                ROUND(CAST(SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS Recruiter_Hiring_Rate_Percent,
                ROUND(AVG(Overall_Score), 2) AS Avg_Overall_Score_Of_Candidates
            FROM Fact_Recruitment_CSV
            GROUP BY Recruiter_Name;
        """)

        # Create SQLite View matching v_Department_Recruitment_Metrics
        cursor.execute("""
            CREATE VIEW IF NOT EXISTS v_Department_Recruitment_Metrics AS
            SELECT 
                Department AS Department_Name,
                COUNT(*) AS Total_Applications,
                SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) AS Hired_Count,
                ROUND(CAST(SUM(CASE WHEN Status = 'Hired' THEN 1 ELSE 0 END) AS FLOAT) * 100.0 / COUNT(*), 2) AS Dept_Hiring_Rate_Percent,
                ROUND(AVG(Age), 1) AS Avg_Candidate_Age,
                ROUND(AVG(Notice_Period), 1) AS Avg_Notice_Period_Days
            FROM Fact_Recruitment_CSV
            GROUP BY Department;
        """)
        
        self.sqlite_conn.commit()
        self.connection_type = "SQLite Database Engine (HR_Recruitment_Dataset_Cleaned.csv)"

    def _clean_value(self, val):
        if isinstance(val, Decimal):
            return float(val)
        return val

    def query(self, sql_query, params=()):
        """Executes query on SQL Server if available, otherwise SQLite."""
        rows = []
        columns = []
        if self.sql_conn:
            try:
                cursor = self.sql_conn.cursor()
                cursor.execute(sql_query, params)
                columns = [column[0] for column in cursor.description]
                raw_rows = cursor.fetchall()
                rows = [dict(zip(columns, [self._clean_value(v) for v in row])) for row in raw_rows]
                return rows
            except Exception as e:
                print(f"MSSQL query failed ({e}), falling back to SQLite...")
                saved_conn_type = self.connection_type
                if not self.sqlite_conn:
                    self._setup_sqlite_engine()
                if saved_conn_type:
                    self.connection_type = saved_conn_type

        cursor = self.sqlite_conn.cursor()
        cursor.execute(sql_query, params)
        columns = [column[0] for column in cursor.description]
        raw_rows = cursor.fetchall()
        rows = [dict(zip(columns, [self._clean_value(v) for v in row])) for row in raw_rows]
        return rows

    def get_status(self):
        return {
            "connected": True,
            "source": self.connection_type,
            "pyodbc_installed": PYODBC_AVAILABLE
        }

db = DatabaseConnector()
