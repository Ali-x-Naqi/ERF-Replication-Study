# Presentation Outline: ERF Framework (5 Minutes)

**Presentation Strategy:** 
You have a strict 5-minute window (4 min speaking + 1 min Q&A). You need to be fast, punchy, and confident. Have your IDE open with `improved_codebase.py` and the `Improvisation_Report.html` open in a browser before you walk up.

---

## Slide 1: Introduction (30 seconds)
* **Title:** Improvised Enhanced Random Forest (ERF) Framework
* **Names:** Ali Naqi (23F-3052) & Muhammad Ahmad (23F-3028) | SE-6B
* **The Paper:** Hussain et al. (2025) - Predicting Mobile App Ratings
* **Hook:** The original paper achieved 85% Accuracy on a tiny, hand-picked sample of 7,000 apps. Our goal was to scale this to a massive dataset and engineer features to match or beat their performance in the real world.

## Slide 2: Original Paper Problems & Technical Hurdles (45 seconds)
* **Original Paper Problem 1 (Tiny Data):** Evaluated on only 7,197 rows, ignoring 99% of the App Store data. This causes complex models to "memorize" data rather than learn, giving artificially inflated accuracy.
* **Original Paper Problem 2 (Basic Features):** Used only raw columns (Price, Size) without extracting meaningful data like App Age or Update Frequency.
* **Our Technical Hurdles:**
  1. **Memory Crashes:** Scaling to 1.2 Million rows caused `loky` multiprocessing ArrayMemoryErrors. We solved this by optimizing data types, dropping useless columns, and careful multi-threading (`n_jobs=-1`).
  2. **Noise in Ratings:** Apps with only 1 or 2 reviews have random, unreliable ratings that destroy model training.

## Slide 3: Our Academic Improvisations (Methodology) (45 seconds)
* **Improvisation 1: IQR Outlier Detection (EDA)**
  * Filtered initial noise (Reviews < 100), then implemented the mathematical **Interquartile Range (IQR)** method to strictly remove statistical outliers in Price and Size, resulting in 57,000 highly robust samples.
* **Improvisation 2: Dimensionality Reduction (PCA)**
  * After feature engineering, we applied **Principal Component Analysis (PCA)**, reducing our feature space to principal components that retain 95% of dataset variance.
* **Improvisation 3: Cross Validation & Hyperparameter Tuning**
  * Replaced basic train-test splits with **Stratified K-Fold Cross Validation**.
  * Replaced manual guessing with **RandomizedSearchCV** to scientifically locate the optimal hyperparameter bounds.

## Slide 4: Replication vs. Improvisation Stats (1 minute)
*Show a table comparing Task 2 vs Task 3 (You can screenshot the table from the HTML report).*
* **The Big Win:** 
  * **Logistic Regression** jumped from a failing **0.43 F1-Score** in Task 2 to **0.92 F1-Score** in Task 3 (+114% gain!).
  * **Random Forest** Accuracy increased to **85.0%** (beating our Task 2 replication on much harder, real-world data).
  * **XGBoost** reached **92% F1-Score** and **85.4% Accuracy**.
* **Key Takeaway:** By engineering domain-specific features and filtering for statistically significant ratings (>=100 reviews), we completely eliminated the negative performance drops and built a highly robust, production-ready classifier.

## Slide 5: Live Demo & Q&A (1 minute)
* **Live Demo Action:** Switch to your terminal. Press `ENTER` to run `python improved_codebase.py`. Show the live output printing the ablation study metrics. Then switch to the browser and show the HTML report.
* **Q&A Readiness:** Be prepared to answer:
  * *"Why did you use Log Transforms?"* -> "Because app reviews range from 100 to 10 million. Log transforms compress this scale so linear models don't get skewed."
  * *"Why remove apps under 100 reviews?"* -> "An app with 1 review of 5-stars isn't a 5-star app, it's just the developer rating their own app. It's statistical noise."
