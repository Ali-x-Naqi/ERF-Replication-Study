# Task 3: Improvisation Difference Log (Data Science Academic Methods)

This document serves as the required **Difference Log** explaining the changes made to transition from our Task 2 (Replication) to Task 3 (Improvisation). 

To ensure strict adherence to the university Data Science curriculum, all improvisations implemented in `improved_codebase.py` map directly to standard syllabus topics.

## Key Academic Changes & Additions

### 1. Data Engineering (Scale & Generalization)
- **Task 2:** Hardcoded to run on a random sample of just 7,197 rows to perfectly match the paper's restricted dataset.
- **Task 3:** Expanded the dataset analysis to a massive **100,000 row** capacity to ensure our models are actually learning, rather than just memorizing a tiny subset.

### 2. Outlier Detection using IQR (Topic: Exploratory Data Analysis)
- **Task 2:** Ignored statistical noise.
- **Task 3:** Implemented mathematical **IQR (Interquartile Range)** outlier detection on continuous variables like `Price` and `Size_Bytes`. This removes extreme outliers that artificially skew model loss functions.

### 3. Dimensionality Reduction (Topic: PCA)
- **Task 2:** Used raw categorical engineered features directly.
- **Task 3:** Applied **Principal Component Analysis (PCA)** to reduce the dense feature space while retaining 95% of the overall data variance. This dramatically decreases multicollinearity and improves model inference speed.

### 4. Robust Evaluation (Topic: K-Fold CV)
- **Task 2:** Basic one-off 80/20 train/test split.
- **Task 3:** Migrated to **Stratified K-Fold Cross Validation (k=3)** to scientifically ensure our accuracy metrics are robust across all folds and immune to random seed luck.

### 5. Automated Hyperparameter Tuning (Topic: Model Tuning)
- **Task 2:** Used static, hardcoded hyperparameters defined in the paper.
- **Task 3:** Integrated **RandomizedSearchCV** to scientifically locate optimal configuration bounds across a grid space for both Random Forest and XGBoost.

## Algorithmic Enhancement (Negative Finding on SMOTE)
We originally integrated the `imbalanced-learn` library to apply **SMOTE** synthetic oversampling. Through our rigorous ablation study, we scientifically proved that SMOTE actually degraded the F1-Score on this specific data distribution. Recognizing negative findings is a core tenet of data science, leading us to confidently exclude it from our final pipeline for superior efficiency and accuracy.
