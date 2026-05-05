# PowerPoint Slide Guide: ERF Framework Improvisation

**Ali Naqi (23F-3052) & Muhammad Ahmad (23F-3028)**

---

## Slide 1: Title Slide
*   **Main Title:** Improvised Enhanced Random Forest (ERF) Framework
*   **Subtitle:** Achieving Superior Generalization using Academic Data Science Methodologies
*   **Presented by:** Ali Naqi & Muhammad Ahmad (Section: SE-6B)
*   **Base Paper:** Hussain et al. (2025)

## Slide 2: Introduction & Objective
*   **The Problem:** Original paper results (85% Accuracy) were limited to a tiny 7,197 row sample.
*   **Our Objective:** 
    1.  Replicate the paper's results (Task 2).
    2.  Scale and "Improvise" using standard Data Science curriculum topics (Task 3).
    3.  Achieve higher metrics on a much larger, realistic dataset.

## Slide 3: Original Paper Limitations
*   **Sample Size:** Only 7,197 apps (Ignoring 99% of App Store data).
*   **Feature Set:** Limited to basic raw columns (Price, Size, Genre).
*   **Evaluation:** Simple train-test split (High risk of overfitting to the specific 7K sample).

## Slide 4: Academic Improvisations (The "How")
*   **Outlier Detection (EDA):** Mathematical **IQR (Interquartile Range)** used to remove extreme price/size noise.
*   **Dimensionality Reduction (PCA):** Applied **Principal Component Analysis** to reduce 46 features to the top 24 components (95% variance).
*   **Validation (Evaluation):** Replaced basic splits with **Stratified K-Fold Cross Validation (k=3)** for stable metrics.
*   **Optimization (Tuning):** Used **RandomizedSearchCV** to scientifically find optimal model parameters.

## Slide 5: Data Engineering & Scaling
*   **Raw Data:** 1,230,376 apps.
*   **Refinement:** Filtered for statistically significant ratings (Reviews >= 100).
*   **Final Dataset:** **57,862 rows** (8x larger than the original paper).
*   **Features:** Added Log Transforms and Interaction features (e.g., Reviews Per Day).

## Slide 6: Results: Replication vs. Improvisation
*(Copy the Table from your HTML report here)*
*   **Logistic Regression:** Huge gain from 0.43 ➔ **0.92 F1-Score**.
*   **Random Forest:** Maintained 85% Accuracy on 8x more data.
*   **The Big Win:** **92% F1-Score** achieved across all models.

## Slide 7: Technical Hurdles & Findings
*   **Memory Management:** Handling 1.2M rows required data-type optimization.
*   **Negative Finding (SMOTE):** We scientifically proved that SMOTE degraded performance on this dataset—demonstrating rigorous model selection.
*   **PCA Efficiency:** Dimensionality reduction allowed complex ensembles to train on 57K rows in under 2 minutes.

## Slide 8: Conclusion
*   Our improvised pipeline proves that **Data Quality (IQR)** and **Feature Engineering (Log/PCA)** are more important than just model complexity.
*   Final Model is **Production Ready**, handles large-scale data, and outperforms the original paper's baseline.

---

### Tips for PowerPoint:
1.  **Use the Graphs:** Take screenshots of `fig1_three_way_comparison.png` and `fig3_ablation_study.png` from the `improved_plots` folder and put them on Slide 6.
2.  **Use the Matrix:** Put `fig2_confusion_matrices.png` on a separate slide if you have time for a deep dive into TP/TN.
3.  **Keep it Simple:** Don't put too much text. Use the bullet points above and speak the details.
