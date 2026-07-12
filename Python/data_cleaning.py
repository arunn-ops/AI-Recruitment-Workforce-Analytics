import os
import pandas as pd

def clean_data():
    print("--- DATA CLEANING MODULE ---")
    
    # Define file paths
    base_dir = "C:\\Users\\Surya\\.gemini\\antigravity\\scratch\\AI-Recruitment-Workforce-Analytics"
    input_path = os.path.join(base_dir, "Dataset", "HR_Recruitment_Dataset.csv")
    output_path = os.path.join(base_dir, "Dataset", "HR_Recruitment_Dataset_Cleaned.csv")
    
    if not os.path.exists(input_path):
        print(f"Error: Raw dataset not found at {input_path}")
        return False
        
    # 1. Load data
    print("1. Loading raw dataset...")
    df = pd.read_csv(input_path)
    print(f"   Initial shape: {df.shape}")
    
    # 2. Check and remove duplicates
    print("2. Checking for duplicate candidates...")
    duplicates_count = df.duplicated(subset=['Candidate_ID']).sum()
    if duplicates_count > 0:
        df = df.drop_duplicates(subset=['Candidate_ID'])
        print(f"   Removed {duplicates_count} duplicate records.")
    else:
        print("   No duplicate Candidate_IDs found.")
        
    # 3. Handle missing values
    print("3. Handling missing values...")
    # Offered_Salary is empty for rejected/applied/interviewed. Let's fill with 0
    df['Offered_Salary'] = df['Offered_Salary'].fillna(0)
    
    # Handle dates: convert to datetime and handle empty fields
    date_cols = ['Application_Date', 'Interview_Date', 'Offer_Date', 'Joining_Date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # Fill empty text columns or numeric scores if any
    # For Applied candidates, Technical_Score, HR_Score, Communication_Score might be empty if we want to represent them.
    # In our dataset generation, they might be empty. Let's fill them with appropriate default (0)
    score_cols = ['Resume_ATS_Score', 'Technical_Score', 'HR_Score', 'Communication_Score']
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    # Calculate/re-verify Overall Score:
    df['Overall_Score'] = (
        df['Resume_ATS_Score'] * 0.20 +
        df['Technical_Score'] * 0.30 +
        df['HR_Score'] * 0.30 +
        df['Communication_Score'] * 0.20
    ).round(2)
    
    # 4. Standardize text columns
    print("4. Standardizing text categories...")
    text_cols = ['Gender', 'Location', 'Education', 'University', 'Job_Role', 
                 'Department', 'Recruitment_Source', 'Status', 'Work_Mode', 'Employment_Type', 'Result']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        
    # 5. Type Conversions
    df['Age'] = df['Age'].astype(int)
    df['Experience'] = df['Experience'].astype(int)
    df['Notice_Period'] = df['Notice_Period'].astype(int)
    df['Expected_Salary'] = df['Expected_Salary'].astype(float)
    df['Offered_Salary'] = df['Offered_Salary'].astype(float)
    
    # Save cleaned file
    print("5. Saving cleaned dataset...")
    df.to_csv(output_path, index=False)
    print(f"   Cleaned dataset saved to: {output_path}")
    print(f"   Final shape: {df.shape}")
    print("Data cleaning complete!\n")
    return True

if __name__ == "__main__":
    clean_data()
