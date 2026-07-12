import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def preprocess_data():
    print("--- PREPROCESSING MODULE ---")
    
    # Paths
    base_dir = "C:\\Users\\Surya\\.gemini\\antigravity\\scratch\\AI-Recruitment-Workforce-Analytics"
    input_path = os.path.join(base_dir, "Dataset", "HR_Recruitment_Dataset_Cleaned.csv")
    output_dir = os.path.join(base_dir, "Dataset", "processed")
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(input_path):
        print(f"Error: Cleaned dataset not found at {input_path}")
        return None
        
    # 1. Load Cleaned Data
    df = pd.read_csv(input_path)
    
    # 2. Define target variable and drop unnecessary columns
    # We want to predict 'Result' (Selected = 1, Rejected = 0)
    df['Target'] = df['Result'].map({'Selected': 1, 'Rejected': 0})
    
    # Features
    numerical_features = ['Age', 'Experience', 'Notice_Period', 'Resume_ATS_Score', 
                          'Technical_Score', 'HR_Score', 'Communication_Score', 
                          'Overall_Score', 'Expected_Salary']
    
    categorical_features = ['Gender', 'Location', 'Education', 'Department', 
                            'Recruitment_Source', 'Work_Mode', 'Employment_Type']
    
    # Select columns
    X = df[numerical_features + categorical_features]
    y = df['Target']
    
    # 3. Train-Test Split (80% Train, 20% Test)
    print("1. Splitting data into Train and Test partitions (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Feature Transformations (One-hot encoding and Standard scaling)
    print("2. Fitting transformations (scaling and one-hot encoding)...")
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )
    
    # Fit and transform
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names after preprocessing
    ohe_categories = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
    all_feature_names = list(numerical_features) + list(ohe_categories)
    
    # 5. Save processed files
    print("3. Saving splits to disk...")
    np.save(os.path.join(output_dir, "X_train.npy"), X_train_processed)
    np.save(os.path.join(output_dir, "X_test.npy"), X_test_processed)
    np.save(os.path.join(output_dir, "y_train.npy"), y_train.values)
    np.save(os.path.join(output_dir, "y_test.npy"), y_test.values)
    
    # Save feature names
    with open(os.path.join(output_dir, "features.txt"), "w") as f:
        f.write("\n".join(all_feature_names))
        
    print(f"   Processed shapes:")
    print(f"   X_train: {X_train_processed.shape}, X_test: {X_test_processed.shape}")
    print(f"   y_train: {y_train.shape}, y_test: {y_test.shape}")
    print("Preprocessing complete!\n")
    return X_train_processed, X_test_processed, y_train, y_test

if __name__ == "__main__":
    preprocess_data()
