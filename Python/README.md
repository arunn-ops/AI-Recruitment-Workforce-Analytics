# Python Machine Learning Module

This module contains the codebase for data cleaning, preprocessing, and training a machine learning classifier to predict whether a candidate will be **Selected** or **Rejected** based on their profile and scores.

## Directory Structure

```
Python/
│
├── data_cleaning.py      # Cleans raw recruitment data, handles missing values & formats types
├── preprocessing.py      # Scales numeric features, encodes categoricals, splits datasets
├── prediction_model.py   # Trains Random Forest model, outputs accuracy and metrics
└── requirements.txt      # List of dependencies
```

## Running the Pipelines

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Clean data**:
   This reads `Dataset/HR_Recruitment_Dataset.csv` and outputs `Dataset/HR_Recruitment_Dataset_Cleaned.csv` with standardized types.
   ```bash
   python data_cleaning.py
   ```

3. **Preprocess and partition data**:
   This normalizes columns, encodes categories, and outputs partitioned numpy arrays inside the `Dataset/processed` folder.
   ```bash
   python preprocessing.py
   ```

4. **Train and evaluate model**:
   This fits a Random Forest Classifier and saves confusion matrix and feature importance plots in `Images/` folder.
   ```bash
   python prediction_model.py
   ```

## Model Targets & Features

- **Target**: `Result` (Selected/Rejected) -> mapped to `1` / `0`
- **Features Used**:
  - *Numerical*: Age, Experience, Notice Period, Resume ATS Score, Technical Score, HR Score, Communication Score, Overall Score, Expected Salary.
  - *Categorical*: Gender, Location, Education, Department, Recruitment Source, Work Mode, Employment Type.
- **Model Choice**: Random Forest Classifier (excellent robustness and outputs feature importances).
