# Final Presentation Script: Improvised ERF Framework

**Speakers:** Ali Naqi & Muhammad Ahmad
**Time Limit:** 5 Minutes

---

### Slide 1: Introduction (Ali Naqi - 30 seconds)
**Ali Naqi:** "Good morning everyone. I am Ali Naqi, and together with my partner Muhammad Ahmad, we are presenting our project on the 'Improvised Enhanced Random Forest Framework.' Our goal was to take a base research paper from 2025 and completely re-engineer the pipeline to handle massive, real-world data using an advanced Ensemble approach."

---

### Slide 2: The Original Paper & The Scalability Gap (Ali Naqi - 45 seconds)
**Ali Naqi:** "The original paper by Hussain et al. reported an 85% accuracy, but there was a major catch: they only evaluated their model on 7,197 apps. In a store of over a million apps, testing on less than 1% leads to extreme overfitting—the model just 'memorizes' the data. We identified this scalability gap as our primary problem to solve."

---

### Slide 3: Our Solution - The 4 Academic Pillars (Muhammad Ahmad - 1 minute)
**Muhammad Ahmad:** "To fix this, we didn't just tweak the model; we rebuilt the data pipeline using 4 pillars from our coursework. First, we used **IQR** to mathematically remove statistical noise—like $999 prank apps. Second, we applied **PCA** to compress 46 complex features into 24 clean principal components. Third, we implemented **Stratified K-Fold Validation**, and finally, we used **RandomizedSearchCV** to scientifically tune our parameters."

---

### Slide 4: The Models & Our New Ensemble Approach (Ali Naqi - 45 seconds)
**Ali Naqi:** "For the models, we used Logistic Regression, Random Forest, and XGBoost. But we wanted to go a step further. We implemented a **Soft Voting Ensemble Classifier**. Instead of relying on a single model, our Ensemble runs all three simultaneously and averages their prediction probabilities—or confidence scores. This ensures that the final prediction is highly stable and robust against any single model's errors."

---

### Slide 5: The Results (Muhammad Ahmad - 1 minute)
**Muhammad Ahmad:** "The results prove our pipeline works. We scaled the dataset to **57,862 rows**. Look at our Logistic Regression: during replication, it failed with a 0.43 F1-Score. But with our clean data and new features, it jumped to 0.92. Our new Soft Voting Ensemble also achieved a rock-solid **92% F1-Score**. We matched the paper's accuracy but on a dataset 8 times larger."

---

### Slide 6: Conclusion (Muhammad Ahmad - 30 seconds)
**Muhammad Ahmad:** "In conclusion, our project proves a fundamental rule of Data Science: Data Quality and Feature Engineering are far more important than Model Complexity. By cleaning the data and using a confidence-based Ensemble, we built a pipeline that is truly production-ready. Thank you, and we are now open for questions."

---

### Q&A Defense Strategy (Both):
*   **Why did you use a Voting Ensemble?** "To maximize stability. By combining LR, RF, and XGBoost using soft voting, we average out their individual weaknesses based on their confidence probabilities."
*   **Why PCA?** "To solve multicollinearity and improve inference speed on the massive 57K dataset."
*   **Why IQR?** "To ensure our model learns from typical apps, not extreme outliers like $999 prank apps."
