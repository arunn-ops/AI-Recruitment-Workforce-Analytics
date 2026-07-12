import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_and_evaluate():
    print("--- MODEL TRAINING & EVALUATION MODULE ---")
    
    # Paths
    base_dir = "C:\\Users\\Surya\\.gemini\\antigravity\\scratch\\AI-Recruitment-Workforce-Analytics"
    processed_dir = os.path.join(base_dir, "Dataset", "processed")
    images_dir = os.path.join(base_dir, "Images")
    screenshots_dir = os.path.join(base_dir, "Documentation", "Screenshots")
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)
    
    # 1. Load data
    print("1. Loading preprocessed arrays...")
    try:
        X_train = np.load(os.path.join(processed_dir, "X_train.npy"))
        X_test = np.load(os.path.join(processed_dir, "X_test.npy"))
        y_train = np.load(os.path.join(processed_dir, "y_train.npy"))
        y_test = np.load(os.path.join(processed_dir, "y_test.npy"))
        
        with open(os.path.join(processed_dir, "features.txt"), "r") as f:
            features = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error loading files: {e}")
        return
        
    print(f"   Train data shape: {X_train.shape}")
    print(f"   Test data shape: {X_test.shape}")
    
    # 2. Train Random Forest Classifier
    print("2. Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # 3. Predict and evaluate
    print("3. Generating predictions...")
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["Rejected", "Selected"])
    
    print(f"\n======================================")
    print(f"MODEL RESULTS:")
    print(f"======================================")
    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"\nClassification Report:")
    print(report)
    print(f"======================================\n")
    
    # 4. Save and plot Confusion Matrix
    print("4. Plotting Confusion Matrix...")
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Rejected", "Selected"], yticklabels=["Rejected", "Selected"])
    plt.title("Candidate Selection Confusion Matrix")
    plt.ylabel("Actual Result")
    plt.xlabel("Predicted Result")
    plt.tight_layout()
    
    cm_path = os.path.join(images_dir, "confusion_matrix.png")
    cm_path_screenshot = os.path.join(screenshots_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.savefig(cm_path_screenshot, dpi=300)
    plt.close()
    print(f"   Confusion matrix saved to: {cm_path}")
    
    # 5. Extract Feature Importances
    print("5. Extracting Feature Importances...")
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Save top 10 features
    top_n = min(10, len(features))
    plt.figure(figsize=(10, 6))
    plt.title("Top 10 Feature Importances for Candidate Selection")
    sns.barplot(x=importances[indices[:top_n]], y=np.array(features)[indices[:top_n]], palette="viridis")
    plt.xlabel("Relative Importance Score")
    plt.tight_layout()
    
    fi_path = os.path.join(images_dir, "feature_importances.png")
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"   Feature importances plotted and saved to: {fi_path}")
    
    print("Top Feature Rank:")
    for rank, idx in enumerate(indices[:top_n], 1):
        print(f"   {rank}. {features[idx]}: {importances[idx]:.4f}")
        
    print("Model training and evaluation complete!\n")

if __name__ == "__main__":
    train_and_evaluate()
