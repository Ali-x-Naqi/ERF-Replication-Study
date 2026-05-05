# Final Presentation Script: Improvised ERF Framework

**Speakers:** Ali Naqi & Muhammad Ahmad
**Total Slides:** 13
**Time Limit:** 5 Minutes (approx. 20-25 seconds per slide)

---

### Slide 1: Title Slide (Ali Naqi)
**Ali Naqi:** "Good morning everyone. I am Ali Naqi, and today, alongside Muhammad Ahmad, we are presenting our project: an 'Improvised Enhanced Random Forest Framework.' Our work goes beyond simple replication to prove how academic Data Science methodologies can drive superior generalization on real-world datasets. As you can see, we achieved a 92% F1-score on a dataset 8 times larger than the original paper."

### Slide 2: The Problem: Scalability Gap (Ali Naqi)
**Ali Naqi:** "The core problem we identified in the 2025 paper by Hussain et al. was a scalability gap. Their model was only tested on 7,197 rows—less than 1% of the available data. This creates a high risk of 'memorization.' Our objective was twofold: first, to faithfully replicate their baseline (Task 2), and second, to improvise using 57,862 rows to prove true model generalization (Task 3)."

### Slide 3: Original Paper Limitations (Ali Naqi)
**Ali Naqi:** "Why was an improvisation necessary? The original paper had several limitations: a microscopic sample size, no outlier handling for extreme prices, a primitive feature set without transforms, and a weak evaluation strategy using simple splits instead of Cross-Validation. This left significant performance—and reliability—on the table."

### Slide 4: Academic Improvisations — The Four Pillars (Ali Naqi)
**Ali Naqi:** "To fix this, we integrated four pillars from our Data Science syllabus. First, **IQR Outlier Detection** to remove noisy data. Second, **PCA** to reduce our 46 features into 24 principal components. Third, **Stratified K-Fold Cross-Validation** for stable metrics. And fourth, **RandomizedSearchCV** to scientifically locate the optimal hyperparameters for our models."

### Slide 5: Data Engineering & Scaling (Ali Naqi)
**Ali Naqi:** "In our engineering phase, we processed over 1.2 million raw apps to extract our final 57,000-row dataset. We applied Log Transforms to normalize skewed review counts and engineered interaction features like 'Reviews Per Day.' Finally, we used PCA to retain 95% of the data variance while keeping the training time under 2 minutes."

### Slide 6: Results: Task 2 vs. Task 3 (Ali Naqi)
**Ali Naqi:** "The results of this engineering were immediate. The most significant win was 'rescuing' Logistic Regression, which jumped from a failing 0.43 F1-score in replication to a massive 0.92 in our improvisation. This proves that high-quality Data Engineering can make even simple models perform at an elite level. I will now hand over to Ahmad to walk us through the detailed metrics."

---

### Slide 7: Chart: Paper vs. Replication vs. Improved (Muhammad Ahmad)
**Muhammad Ahmad:** "Thank you, Ali. Looking at the side-by-side comparison in Figure 1, the green bars represent our Task 3 Improved pipeline. You can see that we uniformly dominate across every single metric—Accuracy, Precision, Recall, and F1. This isn't just luck on one model; our pipeline successfully lifted the performance of all three classifiers simultaneously."

### Slide 8: Chart: Confusion Matrices (Muhammad Ahmad)
**Muhammad Ahmad:** "Our Confusion Matrices in Figure 2 provide the 'ground truth.' With a True Positive rate of approximately 84% and very low False Negatives (under 2%), our models are exceptionally good at identifying 'High-Rated' apps. This high recall is critical for production environments where missing a successful app is more costly than a slight misclassification."

### Slide 9: Chart: Ablation Study (Muhammad Ahmad)
**Muhammad Ahmad:** "Figure 3 shows our Ablation Study, which is the heart of our research. It tracks the F1-score progression as we add each improvement. You can see the massive leap when we introduced IQR-Filtered data. Interestingly, step 4 shows a drop—this is where we tested SMOTE resampling. We found it actually hurt performance, leading us to reject it for a cleaner, real-data approach."

### Slide 10: Chart: Feature Importance (Muhammad Ahmad)
**Muhammad Ahmad:** "Because we used PCA, our feature importance in Figure 4 is based on Principal Components. PC 24 dominates the Gini importance, likely capturing the interaction between app age and review velocity. By using PCA, we ensured that the Random Forest doesn't overfit to noisy raw columns, making the model much more robust to future data changes."

### Slide 11: Chart: Final F1-Scores (Muhammad Ahmad)
**Muhammad Ahmad:** "As shown here, all three models—Logistic Regression, Random Forest, and XGBoost—converged at a near-perfect 0.92 F1-score. This convergence is proof that our data preprocessing and feature engineering were so effective that the choice of algorithm became almost secondary. The intelligence is in the pipeline, not just the model."

### Slide 12: Key Technical Findings (Muhammad Ahmad)
**Muhammad Ahmad:** "Our most valuable 'Negative Finding' was the rejection of SMOTE. We proved that for this distribution, synthetic data adds noise rather than value. On the positive side, our use of IQR was a 'gatekeeper' that drove the biggest gains, and our memory management allowed us to process 1.2 million rows with a 40% reduction in RAM usage."

### Slide 13: Conclusion (Muhammad Ahmad)
**Muhammad Ahmad:** "To conclude, we have proved that Data Quality and Engineering are superior to model complexity. By scaling the paper's dataset by 8 times and achieving a 92.09% F1-score, we have built a framework that is stable, academically sound, and truly production-ready. We are now open for your questions. Thank you."

---

### Q&A Defense:
*   **Ali (IQR):** "We used IQR to make sure extreme outliers (like $999 apps) didn't distort the decision boundaries."
*   **Ahmad (PCA):** "PCA allowed us to retain 95% of the information while reducing the feature count from 46 to 24, making the training 5x faster."
