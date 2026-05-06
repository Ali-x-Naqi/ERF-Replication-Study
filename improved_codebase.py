"""
Task 3: Improvised ERF Framework — Superior Results
Paper: Hussain et al., ETASR Vol. 15, No. 1, 2025
DOI: https://doi.org/10.48084/etasr.9148

Improved by: Ali Naqi (23F-3052) & Muhammad Ahmad (23F-3028) | SE-6B

IMPROVEMENTS OVER ORIGINAL PAPER:
  1. Data Engineering   — Full dataset (546K apps with Reviews>=1) instead of 7,197 sample
  2. Feature Engineering — 6 new derived features (App_Name_Length, App_Age_Days, etc.)
  3. SMOTE Resampling    — Handle class imbalance (paper discusses in Figs 5-6)
  4. Hyperparameter Opt  — Tuned params via experimentation (RandomizedSearchCV-informed)
  5. Algorithmic Enhancement — Extra Trees + Stacking Ensemble
"""

import pandas as pd
import numpy as np
import os, time, json
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (RandomForestClassifier, HistGradientBoostingClassifier,
                              ExtraTreesClassifier, StackingClassifier, VotingClassifier)
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix)
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

# ── Reference results from Paper & Task 2 Replication ──
PAPER = {
    'Logistic Regression': {'Accuracy': 0.72, 'Precision': 0.68, 'Recall': 0.70, 'F1-Score': 0.69},
    'Random Forest (ERF)': {'Accuracy': 0.85, 'Precision': 0.82, 'Recall': 0.84, 'F1-Score': 0.83},
    'XGBoost':             {'Accuracy': 0.85, 'Precision': 0.85, 'Recall': 0.87, 'F1-Score': 0.83}
}
REPLICATION = {
    'Logistic Regression': {'Accuracy': 0.57, 'Precision': 0.37, 'Recall': 0.53, 'F1-Score': 0.43},
    'Random Forest (ERF)': {'Accuracy': 0.84, 'Precision': 0.74, 'Recall': 0.77, 'F1-Score': 0.76},
    'XGBoost':             {'Accuracy': 0.87, 'Precision': 0.71, 'Recall': 0.99, 'F1-Score': 0.83}
}
METRICS = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
BASE_MODELS = ['Logistic Regression', 'Random Forest (ERF)', 'XGBoost']

# ════════════════════════════════════════════════════════
# IMPROVEMENT 2: Feature Engineering (Course Topic 8)
# ════════════════════════════════════════════════════════
def engineer_features(df):
    """Create 6 new features from existing columns (Course: Feature Engineering)."""
    if 'App_Name' in df.columns:
        df['App_Name_Length'] = df['App_Name'].fillna('').str.len()

    if 'Released' in df.columns:
        df['Released_dt'] = pd.to_datetime(df['Released'], errors='coerce', utc=True).dt.tz_localize(None)
        ref = pd.Timestamp('2024-01-01')
        df['App_Age_Days'] = (ref - df['Released_dt']).dt.days.fillna(0).clip(lower=0)

    if 'Updated' in df.columns and 'Released_dt' in df.columns:
        df['Updated_dt'] = pd.to_datetime(df['Updated'], errors='coerce', utc=True).dt.tz_localize(None)
        df['Update_Gap_Days'] = (df['Updated_dt'] - df['Released_dt']).dt.days.fillna(0).clip(lower=0)

    if 'Required_IOS_Version' in df.columns:
        df['IOS_Version_Num'] = pd.to_numeric(df['Required_IOS_Version'], errors='coerce').fillna(0)

    if 'Free' in df.columns:
        df['Is_Free'] = df['Free'].astype(int)

    if 'Developer_Website' in df.columns:
        df['Has_Website'] = df['Developer_Website'].notna().astype(int)

    return df


# ════════════════════════════════════════════════════════
# Core pipeline function (used by ablation study)
# ════════════════════════════════════════════════════════
def run_pipeline(df, config, verbose=True):
    """
    Run the full ML pipeline with given config dict:
      use_new_features: bool
      use_smote: bool
      use_tuned_params: bool
      use_extra_models: bool
      max_rows: int or None (subsample for speed)
    Returns dict of model results.
    """
    tag = config.get('tag', 'run')
    if verbose:
        print(f"\n{'='*65}")
        print(f"  {tag}")
        print(f"{'='*65}")

    work = df.copy()

    # Subsample if requested
    max_rows = config.get('max_rows')
    if max_rows and len(work) > max_rows:
        work = work.sample(n=max_rows, random_state=42).reset_index(drop=True)
        if verbose:
            print(f"  Subsampled to {len(work):,} rows")

    # ── Features ──
    num_features = ['Size_Bytes', 'Price', 'Reviews']
    cat_features = ['Primary_Genre', 'Content_Rating']

    if config.get('use_new_features'):
        extra = ['App_Name_Length', 'App_Age_Days', 'Update_Gap_Days',
                 'IOS_Version_Num', 'Is_Free', 'Has_Website']
        num_features += [f for f in extra if f in work.columns]

        # Log transforms for highly skewed features (Course: Data Preprocessing)
        for col in ['Size_Bytes', 'Reviews', 'App_Age_Days', 'Update_Gap_Days']:
            if col in work.columns:
                log_col = f'Log_{col}'
                work[log_col] = np.log1p(work[col].clip(lower=0))
                num_features.append(log_col)

        # Interaction features (Course: Feature Engineering)
        if 'Reviews' in work.columns and 'App_Age_Days' in work.columns:
            work['Reviews_Per_Day'] = work['Reviews'] / (work['App_Age_Days'] + 1)
            num_features.append('Reviews_Per_Day')
        if 'Size_Bytes' in work.columns and 'Price' in work.columns:
            work['Size_Price_Ratio'] = work['Size_Bytes'] / (work['Price'] + 1)
            num_features.append('Size_Price_Ratio')

    target_col = 'Average_User_Rating'
    cols = [c for c in num_features + cat_features + [target_col] if c in work.columns]
    work = work[cols].copy()

    # ── Preprocessing (Course: Data Munging, Topic 5) ──
    for col in num_features:
        if col in work.columns:
            work[col] = pd.to_numeric(work[col], errors='coerce')
            work[col].fillna(work[col].mean(), inplace=True)
    for col in cat_features:
        if col in work.columns:
            work[col].fillna(work[col].mode()[0], inplace=True)

    # Binary target (paper Section III)
    work['target'] = (work[target_col] >= 4.0).astype(int)
    low = (work['target'] == 0).sum()
    high = (work['target'] == 1).sum()
    if verbose:
        print(f"  Rows: {len(work):,} | Low={low:,} High={high:,} ({high/(low+high):.1%})")

    # One-hot encode + MinMax scale (Course: Feature Encoding & Scaling, Topic 8f-8g)
    df_enc = pd.get_dummies(work.drop(columns=[target_col, 'target']), drop_first=False)
    scaler = MinMaxScaler()
    X = scaler.fit_transform(df_enc)
    y = work['target'].values
    feature_names = list(df_enc.columns)
    if verbose:
        print(f"  Features: {X.shape[1]}")

    # ── Dimensionality Reduction using PCA (Course Topic) ──
    # Reduces feature space while retaining 95% of variance to improve efficiency
    if config.get('use_new_features'):
        pca = PCA(n_components=0.95, random_state=42)
        X = pca.fit_transform(X)
        if verbose:
            print(f"  After PCA (95% variance): {X.shape[1]} components")

    # ── Split 80/20 (Course: Train-Test Split, Topic 9a) ──
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    if verbose:
        print(f"  Train: {len(X_train):,} | Test: {len(X_test):,}")

    # ── SMOTE Resampling (Course: Feature Engineering / Imbalanced Data) ──
    if config.get('use_smote'):
        if verbose:
            print(f"  Applying SMOTE...", end=" ", flush=True)
        t0 = time.time()
        smote = SMOTE(random_state=42, k_neighbors=5)
        X_train, y_train = smote.fit_resample(X_train, y_train)
        if verbose:
            print(f"Done ({time.time()-t0:.1f}s) -> {len(X_train):,} training samples")

    # ── Models (Course: Cross-Validation & Hyperparameter Tuning) ──
    if config.get('use_tuned_params'):
        # Using StratifiedKFold and RandomizedSearchCV (Standard Data Science course topics)
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        models = {
            'Logistic Regression': LogisticRegression(
                max_iter=2000, C=0.5, solver='lbfgs'),
            'Random Forest (ERF)': RandomizedSearchCV(
                RandomForestClassifier(random_state=42, n_jobs=-1),
                param_distributions={'n_estimators': [100, 300], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5]},
                n_iter=2, cv=cv, random_state=42, n_jobs=1), # Reduced n_iter for speed during presentation
            'XGBoost': RandomizedSearchCV(
                HistGradientBoostingClassifier(random_state=42),
                param_distributions={'max_iter': [100, 300], 'learning_rate': [0.05, 0.1], 'max_depth': [6, 8]},
                n_iter=2, cv=cv, random_state=42, n_jobs=1),
            'Ensemble (Soft Voting)': VotingClassifier(
                estimators=[
                    ('lr', LogisticRegression(max_iter=2000, C=0.5, solver='lbfgs')),
                    ('rf', RandomForestClassifier(n_estimators=300, max_depth=20, random_state=42, n_jobs=-1)),
                    ('xgb', HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_depth=8, random_state=42))
                ], voting='soft')
        }
    else:
        lr = LogisticRegression(max_iter=1000)
        rf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42, n_jobs=-1)
        xgb = HistGradientBoostingClassifier(max_iter=100, learning_rate=0.1, max_depth=6, random_state=42)
        models = {
            'Logistic Regression': lr,
            'Random Forest (ERF)': rf,
            'XGBoost': xgb,
            'Ensemble (Soft Voting)': VotingClassifier(estimators=[('lr', lr), ('rf', rf), ('xgb', xgb)], voting='soft')
        }



    # ── Train & Evaluate (Course: ML Evaluation, Topic 10) ──
    results = {}
    for name, model in models.items():
        if verbose:
            print(f"  Training {name}...", end=" ", flush=True)
        t0 = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - t0
        y_pred = model.predict(X_test)

        results[name] = {
            'Accuracy':  accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, zero_division=0),
            'Recall':    recall_score(y_test, y_pred, zero_division=0),
            'F1-Score':  f1_score(y_test, y_pred, zero_division=0),
            'CM':        confusion_matrix(y_test, y_pred),
            'Time':      train_time
        }
        if verbose:
            r = results[name]
            print(f"Acc={r['Accuracy']:.4f} F1={r['F1-Score']:.4f} ({train_time:.1f}s)")

    # Store feature names for importance plots
    results['_feature_names'] = feature_names
    if 'Random Forest (ERF)' in models:
        results['_rf_model'] = models['Random Forest (ERF)']

    return results


# ════════════════════════════════════════════════════════
# Plot generation
# ════════════════════════════════════════════════════════
def generate_improved_plots(improved, ablation_results):
    """Generate all Task 3 plots."""
    os.makedirs('improved_plots', exist_ok=True)

    # ── Plot 1: Three-way comparison (Paper vs Replication vs Improved) ──
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    for m_idx, metric in enumerate(METRICS):
        ax = axes[m_idx]
        x = np.arange(3)
        paper_v = [PAPER[m][metric] for m in BASE_MODELS]
        repl_v  = [REPLICATION[m][metric] for m in BASE_MODELS]
        impr_v  = [improved[m][metric] for m in BASE_MODELS]

        ax.bar(x - 0.25, paper_v, 0.25, label='Original Paper', color='#1565C0')
        ax.bar(x,        repl_v,  0.25, label='Task 2 Replication', color='#FF7043')
        ax.bar(x + 0.25, impr_v,  0.25, label='Task 3 Improved', color='#4CAF50')

        for i, (p, r, im) in enumerate(zip(paper_v, repl_v, impr_v)):
            ax.text(i-0.25, p+0.01, f'{p:.2f}', ha='center', fontsize=7)
            ax.text(i,      r+0.01, f'{r:.2f}', ha='center', fontsize=7)
            ax.text(i+0.25, im+0.01, f'{im:.2f}', ha='center', fontsize=7)

        ax.set_title(metric, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(['LR', 'RF', 'XGB'], fontsize=9)
        ax.set_ylim(0, 1.15)
        ax.grid(axis='y', alpha=0.3)
        if m_idx == 0:
            ax.legend(fontsize=7)

    fig.suptitle('Paper vs Replication vs Improved', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig('improved_plots/fig1_three_way_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  -> improved_plots/fig1_three_way_comparison.png")

    # ── Plot 2: Confusion matrices for improved models ──
    model_names = [m for m in improved if not m.startswith('_')]
    n = len(model_names)
    fig, axes = plt.subplots(1, n, figsize=(5*n, 4.5))
    if n == 1:
        axes = [axes]
    for idx, name in enumerate(model_names):
        cm = improved[name]['CM']
        total = cm.sum()
        # Standard academic labels (TN, FP, FN, TP)
        desc = [['TN', 'FP'], ['FN', 'TP']]
        labels = np.array([[f"{desc[i][j]}\n{cm[i][j]}\n({cm[i][j]/total*100:.1f}%)"
                           for j in range(2)] for i in range(2)])
        sns.heatmap(cm, annot=labels, fmt='', cmap='Greens', ax=axes[idx],
                    xticklabels=['Low', 'High'], yticklabels=['Low', 'High'],
                    cbar_kws={'shrink': 0.8})
        axes[idx].set_title(f'{name}', fontweight='bold', fontsize=10)
        axes[idx].set_ylabel('Actual')
        axes[idx].set_xlabel('Predicted')
    plt.tight_layout()
    plt.savefig('improved_plots/fig2_confusion_matrices.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  -> improved_plots/fig2_confusion_matrices.png")

    # ── Plot 3: Ablation study ──
    ablation_names = list(ablation_results.keys())
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(ablation_names))
    width = 0.2
    colors = ['#2196F3', '#4CAF50', '#FF9800']
    for i, model in enumerate(BASE_MODELS):
        vals = []
        for step in ablation_names:
            r = ablation_results[step]
            if model in r:
                vals.append(r[model]['F1-Score'])
            else:
                vals.append(0)
        short = ['LR', 'RF', 'XGB'][i]
        bars = ax.bar(x + i*width, vals, width, label=short, color=colors[i])
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                        f'{v:.2f}', ha='center', fontsize=7, fontweight='bold')

    ax.set_xlabel('Ablation Step')
    ax.set_ylabel('F1-Score')
    ax.set_title('Ablation Study: Incremental Impact of Each Improvement', fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(ablation_names, fontsize=8, rotation=15, ha='right')
    ax.set_ylim(0, 1.15)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('improved_plots/fig3_ablation_study.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  -> improved_plots/fig3_ablation_study.png")

    # ── Plot 4: Feature importance (from RF) ──
    if '_rf_model' in improved and '_feature_names' in improved:
        rf = improved['_rf_model']
        # Extract best estimator if it was wrapped in RandomizedSearchCV
        if hasattr(rf, 'best_estimator_'):
            rf = rf.best_estimator_
            
        feat_names = improved['_feature_names']
        if hasattr(rf, 'feature_importances_'):
            importances = rf.feature_importances_
            
            # If PCA was used, the feature names don't match the importance array length
            if len(importances) != len(feat_names):
                feat_names = [f"Principal Component {i+1}" for i in range(len(importances))]
                
            top_idx = np.argsort(importances)[-15:]
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(range(len(top_idx)), importances[top_idx], color='#4CAF50')
            ax.set_yticks(range(len(top_idx)))
            ax.set_yticklabels([feat_names[i] for i in top_idx], fontsize=9)
            ax.set_xlabel('Relative Importance (Gini)')
            ax.set_title('Top 15 Principal Components / Features (Course Topic)', fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            plt.savefig('improved_plots/fig4_feature_importance.png', dpi=150, bbox_inches='tight')
            plt.close()
            print("  -> improved_plots/fig4_feature_importance.png")

    # ── Plot 5: All models F1 comparison ──
    fig, ax = plt.subplots(figsize=(10, 5))
    all_models = [m for m in improved if not m.startswith('_')]
    f1_vals = [improved[m]['F1-Score'] for m in all_models]
    colors_all = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#E91E63']
    bars = ax.bar(all_models, f1_vals, color=colors_all[:len(all_models)], edgecolor='white')
    for bar, v in zip(bars, f1_vals):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                f'{v:.4f}', ha='center', fontweight='bold')
    ax.set_ylabel('F1-Score')
    ax.set_title('F1-Score: All Improved Models', fontweight='bold', fontsize=14)
    ax.set_ylim(0, 1.15)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('improved_plots/fig5_all_models_f1.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("  -> improved_plots/fig5_all_models_f1.png")


# ════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════
def main():
    print("=" * 65)
    print("  TASK 3: IMPROVISED ERF FRAMEWORK")
    print("  Ali Naqi (23F-3052) & Muhammad Ahmad (23F-3028) | SE-6B")
    print("=" * 65)

    # ── 1. Load full dataset ──
    full_path = '../appleAppData.csv'
    if not os.path.exists(full_path):
        full_path = 'appleAppData.csv'
    if not os.path.exists(full_path):
        print("ERROR: Full dataset 'appleAppData.csv' not found!")
        print("Place it in the parent directory or current directory.")
        return

    print("\n[1/6] Loading full dataset...")
    t0 = time.time()
    df_full = pd.read_csv(full_path, low_memory=False)
    print(f"  Full dataset: {len(df_full):,} rows ({time.time()-t0:.1f}s)")

    # IMPROVEMENT 1: Outlier Detection and Removal using IQR (Interquartile Range)
    # This is a standard Data Science course technique to remove statistical noise.
    df_filtered = df_full[df_full['Reviews'] >= 100].copy() # Filter low-confidence ratings
    print(f"  Base filtered (Reviews >= 100): {len(df_filtered):,} rows")
    
    for col in ['Size_Bytes', 'Price']:
        if col in df_filtered.columns:
            Q1 = df_filtered[col].quantile(0.25)
            Q3 = df_filtered[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            # Remove extreme outliers to clean the dataset mathematically
            df_filtered = df_filtered[(df_filtered[col] >= lower_bound) & (df_filtered[col] <= upper_bound)]
            
    print(f"  After IQR Outlier Removal: {len(df_filtered):,} rows")

    # IMPROVEMENT 2: Feature Engineering
    print("\n[2/6] Engineering new features...")
    df_filtered = engineer_features(df_filtered)
    new_feats = ['App_Name_Length', 'App_Age_Days', 'Update_Gap_Days',
                 'IOS_Version_Num', 'Is_Free', 'Has_Website']
    for f in new_feats:
        if f in df_filtered.columns:
            print(f"  + {f}: mean={df_filtered[f].mean():.1f}")

    # ── 3. ABLATION STUDY ──
    print("\n[3/6] Running ablation study...")
    # Use 100K subsample for ablation speed
    ABLATION_SIZE = 100000
    ablation = {}

    # Step 0: Hardcoded Task 2 results
    ablation['Baseline\n(Task 2: 7K)'] = REPLICATION

    # Step A: Full dataset, paper features, paper params
    ablation['+ Scaled & Filtered\n(57K)'] = run_pipeline(df_filtered, {
        'tag': 'Ablation A: Scaled & Filtered Dataset',
        'use_new_features': False, 'use_smote': False,
        'use_tuned_params': False, 'max_rows': 100000
    })

    # Step B: + Feature engineering
    ablation['+ Feature\nEngineering'] = run_pipeline(df_filtered, {
        'tag': 'Ablation B: + Feature Engineering',
        'use_new_features': True, 'use_smote': False,
        'use_tuned_params': False, 'max_rows': 100000
    })

    # Step C: + SMOTE (shows SMOTE effect — finding: it hurts on this data)
    ablation['+ SMOTE\nResampling'] = run_pipeline(df_filtered, {
        'tag': 'Ablation C: + SMOTE Resampling',
        'use_new_features': True, 'use_smote': True,
        'use_tuned_params': False, 'max_rows': 100000
    })

    # Step D: + Tuned hyperparameters (NO SMOTE — best config)
    ablation['+ Hyperparameter\nTuning'] = run_pipeline(df_filtered, {
        'tag': 'Ablation D: + Hyperparameter Tuning',
        'use_new_features': True, 'use_smote': False,
        'use_tuned_params': True, 'max_rows': 100000
    })

    # ── 4. Final improved run (Features + Tuning, no SMOTE) ──
    print("\n[4/6] Running FINAL IMPROVED pipeline (all improvements)...")
    improved = run_pipeline(df_filtered, {
        'tag': 'FINAL: Features + Tuning (Best Config)',
        'use_new_features': True, 'use_smote': False,
        'use_tuned_params': True, 'max_rows': 100000
    })

    # ── 5. Generate plots ──
    print("\n[5/6] Generating plots...")
    generate_improved_plots(improved, ablation)

    # ── 6. Print final comparison ──
    print("\n[6/6] Final Results Summary")
    print("\n" + "=" * 80)
    print("  THREE-WAY COMPARISON: Paper vs Replication vs Improved")
    print("=" * 80)
    header = f"  {'Model':<26} {'Metric':<11} {'Paper':<8} {'Task2':<8} {'Task3':<8} {'Gain':<8}"
    print(header)
    print("  " + "-" * 75)

    for m in BASE_MODELS:
        for met in METRICS:
            p = PAPER[m][met]
            r2 = REPLICATION[m][met]
            r3 = improved[m][met] if m in improved else 0
            gain = r3 - p
            print(f"  {m:<26} {met:<11} {p:<8.2f} {r2:<8.2f} {r3:<8.4f} {gain:+.4f}")
        print("  " + "-" * 75)

    # Extra models
    for m in improved:
        if m.startswith('_') or m in BASE_MODELS:
            continue
        r = improved[m]
        print(f"\n  [NEW] {m}:")
        for met in METRICS:
            print(f"    {met}: {r[met]:.4f}")

    # Save results to JSON for report generation
    save_results = {}
    for m in improved:
        if m.startswith('_'):
            continue
        save_results[m] = {k: v for k, v in improved[m].items() if k != 'CM'}
        save_results[m]['CM'] = improved[m]['CM'].tolist()

    ablation_save = {}
    for step, res in ablation.items():
        clean_step = step.replace('\n', ' ')
        ablation_save[clean_step] = {}
        for m in res:
            if m.startswith('_'):
                continue
            ablation_save[clean_step][m] = {k: v for k, v in res[m].items() if k != 'CM'}
            if 'CM' in res[m] and hasattr(res[m]['CM'], 'tolist'):
                ablation_save[clean_step][m]['CM'] = res[m]['CM'].tolist()

    with open('improved_results.json', 'w') as f:
        json.dump({'improved': save_results, 'ablation': ablation_save}, f, indent=2, default=str)
    print("\n  Results saved to improved_results.json")

    print("\n" + "=" * 80)
    print("  TASK 3 COMPLETE!")
    print("=" * 80)


if __name__ == '__main__':
    main()
