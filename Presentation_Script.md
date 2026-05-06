# Final Presentation Script (Roman Urdu)
**Project:** Improvised Enhanced Random Forest (ERF) Framework
**Speakers:** Ali Naqi & Muhammad Ahmad

*Yeh script 9-slide structure ke mutabiq design ki gayi hai. Har slide ka estimated time aur kis ne kya bolna hai, clearly mention kiya gaya hai.*

---

### Slide 1: Title Slide
**Speaker:** Ali Naqi
**Time:** ~30 seconds

"Assalam o Alaikum everyone. Mera naam Ali Naqi hai, aur mere saath Muhammad Ahmad present kar rahe hain. Aaj hum apne Data Science project 'Improvised Enhanced Random Forest Framework' ko present karenge. Hamara main goal tha Hussain et al. ki ek research paper ko replicate karna aur phir advanced Data Engineering aur 'Ensemble Modeling' ke zariye uski generalization ko improve karna. Chaliye shuru karte hain."

---

### Slide 2: The Original Research Paper
**Speaker:** Ali Naqi
**Time:** ~30 seconds

"Sab se pehle dekhte hain original paper kya tha. Hussain et al. ne 2025 mein ek paper publish kiya jiska maqsad tha Apple App Store ki ratings predict karna ke wo 'High' hongi ya 'Low'. Unhone Logistic Regression, XGBoost aur Enhanced Random Forest (ERF) models use kiye aur 85% accuracy claim ki. Lekin is paper mein ek bohot bada flaw tha."

---

### Slide 3: The Problem (Scalability Gap & Overfitting)
**Speaker:** Ali Naqi
**Time:** ~45 seconds

"Wo flaw tha inka microscopic dataset. Unhone poore app store mein se sirf 7,197 apps use ki thein—jo 1% se bhi kam hai. Problem yeh hai ke itne kam data par models rules seekhne ke bajaye data ko 'memorize' kar lete hain, jisay hum overfitting kehte hain. Hamara objective tha ke hum is data ko massively scale karein—taakebataya ja sake ke ek model real-world mein, 57,000+ apps par kaisa perform karega."

---

### Slide 4: Our Improvisation Pipeline
**Speaker:** Muhammad Ahmad
**Time:** ~50 seconds

"Thank you Ali. Main Muhammad Ahmad hoon. Is scalability gap ko theek karne ke liye humne Data Science course ki 4 techniques apply kiye:
1. **IQR:** Sab se pehle humne IQR se statistical outliers remove kiye, jaise kuch apps $999 ki thein jo data ko kharab kar rahi thein.
2. **PCA:** Humne 46 complex features banaye aur phir dimensionality reduction ke zariye unhe 24 clean components mein badal diya.
3. **K-Fold:** Humne simple lucky split par bharosa karne ke bajaye Stratified K-Fold cross validation use ki.
4. **Tuning:** Aur akhir mein parameters ko scientifically tune kiya."

---

### Slide 5: The Models Used & Why
**Speaker:** Muhammad Ahmad
**Time:** ~45 seconds

"Models ke liye humne paper wale teeno base models (LR, RF, XGBoost) use kiye, lekin humne ek step aagay barh kar apna naya **'Soft Voting Ensemble'** model introduce kiya. 
Humne Ensemble kyun banaya? Kyunke ek model par rely karne ke bajaye, hamara Ensemble in teeno models ko ek saath chalata hai aur unke confidence scores (ya probabilities) ki average nikalta hai. Is approach se errors minimize hotay hain aur final prediction maximum stable ho jati hai."

---

### Slide 6: The Results (Comparison)
**Speaker:** Ali Naqi
**Time:** ~45 seconds

"Ab aate hain Results par. Jab humne purane data par Replication (Task 2) ki thi, toh Logistic Regression completely fail ho gaya tha with 0.43 F1-Score. Lekin jab humne apni clean 57K dataset wali pipeline lagayi, toh wahi Logistic Regression 0.92 par jump kar gaya! Aur hamara naya Soft Voting Ensemble bhi rock-solid 92% F1-Score de raha hai—wo bhi original paper se 8 guna zyada data par."

---

### Slide 7: Ablation & Feature Insights
**Speaker:** Ali Naqi
**Time:** ~30 seconds

"Ablation study se humein clear evidence mili ke yeh improvement kahan se aayi. Sab se bada performance jump tab aya jab humne IQR filtering apply ki. Is se saabit hota hai ke Data Quality, Model Complexity se kahin zyada important hai. Aur PCA ne hamare model ko noise se bacha kar aur zyada efficient bana diya."

---

### Slide 8: Detailed Model Performance
**Speaker:** Muhammad Ahmad
**Time:** ~30 seconds

"Confusion Matrices bhi hamari success ko prove karti hain. Hamari True Positive rate bohot high hai aur False Negatives sirf 1-2% hain. Iska matlab hai ke hamara pipeline production-ready hai aur galti se kisi achi app ko low-rating classify karne ke chances bohot kam hain."

---

### Slide 9: Conclusion
**Speaker:** Muhammad Ahmad
**Time:** ~45 seconds

"To conclude, humne 3 cheezein saabit ki hain:
Pehla: Humne framework ki scalability prove kar di hai 57,000 apps par.
Doosra: Model ki algorithm se zyada IQR aur Feature Engineering matter karti hai.
Teesra: Soft Voting Ensemble ka use prediction ko sab se zyada reliable aur stable banata hai.
Thank you very much. Now we are open to any questions."

---

### Extras (Q&A Tip)
*Agar teacher pooche ke Soft Voting Ensemble hi kyun use kiya, toh confidently jawab dain:* "Sir, Hard Voting sirf majority class dekhti hai, lekin Soft Voting har model ke andar ki 'Probability' dekhti hai. Agar ek model 90% sure hai aur baaki do sirf 51% sure hain, toh Soft Voting 90% walay ki baat ko zyada weight de gi. Yeh tareeqa inherently zyada smart aur stable hai."
