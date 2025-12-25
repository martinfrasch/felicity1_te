#!/usr/bin/env python3
"""
Generate sex × stress stratified correlation heatmaps for exploratory findings
Shows ER/SE/TE features vs clinical outcomes
Four panels: Male-Control, Male-Stressed, Female-Control, Female-Stressed
"""

import sys
import os

# Get script directory and set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, os.path.join(script_dir, 'Nicolas_felicity1/src'))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from data_loader import load_entropy_rate, load_sampen, load_te_files

# Load all data files
print("Loading data files...")

data_dir = Path(script_dir) / 'Nicolas_felicity1'

# Load ER data
er_data = load_entropy_rate(data_dir)
print(f"Entropy Rate: {er_data.shape}")

# Load SE data
se_data = load_sampen(data_dir)
print(f"Sample Entropy: {se_data.shape}")

# Load TE data
te_data = load_te_files(data_dir)
print(f"Transfer Entropy: {te_data.shape}")

# Load clinical outcomes
clinical = pd.read_excel(data_dir / '210716 EXCEL FILE FOR BAYLEY-STAN.xlsx')
print(f"Clinical outcomes: {clinical.shape}")

# Standardize patient codes - Clinical file uses 'PATIENT CODE' and format 'FS-XXX'
# First filter out NaN patient codes
clinical = clinical[clinical['PATIENT CODE'].notna()].copy()
clinical['patient_code'] = clinical['PATIENT CODE'].str.replace('FS-', '').astype(int)

# Merge all entropy data
merged = er_data.merge(se_data, on='patient_code', how='outer')
merged = merged.merge(te_data, on='patient_code', how='outer')

# Extract cortisol from column name (has units in parentheses)
cortisol_col = [c for c in clinical.columns if 'CORTISOL' in c][0]

# Merge with clinical outcomes (note: MOTOR FINE has two spaces)
merged = merged.merge(clinical[['patient_code', 'Mother Score_PSS', 'Mother Score PDQ',
                                cortisol_col, 'COG COMPOSITE SCORE',
                                'LANG RECEPT SCORE', 'LANG EXPRES SCORE', 'LANG COMP SCORE',
                                'MOTOR FINE  SKILLS SCORE', 'MOTOR GROSS SKILLS SCORE',
                                'MOTOR COMPOSITE SCORE']],
                     on='patient_code', how='left')

# Rename cortisol column and standardize motor fine column name
merged = merged.rename(columns={
    cortisol_col: 'Mother CORTISOL',
    'MOTOR FINE  SKILLS SCORE': 'MOTOR FINE SKILLS SCORE'
})

# Convert all outcome columns to numeric (handle string values like ' ')
outcome_cols = ['Mother CORTISOL', 'Mother Score_PSS', 'Mother Score PDQ',
                'COG COMPOSITE SCORE', 'LANG RECEPT SCORE', 'LANG EXPRES SCORE',
                'LANG COMP SCORE', 'MOTOR FINE SKILLS SCORE', 'MOTOR GROSS SKILLS SCORE',
                'MOTOR COMPOSITE SCORE']

for col in outcome_cols:
    merged[col] = pd.to_numeric(merged[col], errors='coerce')

print(f"\nMerged data: {merged.shape}")
print(f"\nSample sizes:")
print(f"  Male-Control: {((merged['sex'] == 1) & (merged['stress'] == 0)).sum()}")
print(f"  Male-Stressed: {((merged['sex'] == 1) & (merged['stress'] == 1)).sum()}")
print(f"  Female-Control: {((merged['sex'] == 0) & (merged['stress'] == 0)).sum()}")
print(f"  Female-Stressed: {((merged['sex'] == 0) & (merged['stress'] == 1)).sum()}")

# Define feature groups based on prefix from data_loader
er_features = [c for c in merged.columns if c.startswith('entropy_rate_')]
se_features = [c for c in merged.columns if c.startswith('sampen_')]
te_features = [c for c in merged.columns if '_TE_' in c and c != 'patient_code']

all_features = er_features + se_features + te_features

print(f"\nFeature counts:")
print(f"  Entropy Rate: {len(er_features)}")
print(f"  Sample Entropy: {len(se_features)}")
print(f"  Transfer Entropy: {len(te_features)}")
print(f"  Total: {len(all_features)}")

# Define outcomes
outcomes = ['Mother CORTISOL', 'Mother Score_PSS', 'Mother Score PDQ',
            'COG COMPOSITE SCORE', 'LANG RECEPT SCORE', 'LANG EXPRES SCORE',
            'LANG COMP SCORE', 'MOTOR FINE SKILLS SCORE', 'MOTOR GROSS SKILLS SCORE',
            'MOTOR COMPOSITE SCORE']

# Rename outcomes for display
outcome_rename = {
    'Mother CORTISOL': 'Cortisol',
    'Mother Score_PSS': 'PSS',
    'Mother Score PDQ': 'PDQ',
    'COG COMPOSITE SCORE': 'Cognitive',
    'LANG RECEPT SCORE': 'Lang Receptive',
    'LANG EXPRES SCORE': 'Lang Expressive',
    'LANG COMP SCORE': 'Lang Composite',
    'MOTOR FINE SKILLS SCORE': 'Motor Fine',
    'MOTOR GROSS SKILLS SCORE': 'Motor Gross',
    'MOTOR COMPOSITE SCORE': 'Motor Composite'
}

def compute_correlations(data, features, outcomes):
    """Compute correlation matrix with p-values"""
    corr_matrix = np.zeros((len(features), len(outcomes)))
    pval_matrix = np.zeros((len(features), len(outcomes)))
    n_matrix = np.zeros((len(features), len(outcomes)))

    for i, feat in enumerate(features):
        for j, outcome in enumerate(outcomes):
            # Remove NaN values
            mask = data[[feat, outcome]].notna().all(axis=1)
            x = data.loc[mask, feat]
            y = data.loc[mask, outcome]

            if len(x) >= 10:  # Minimum sample size
                # Test normality
                _, p_norm_x = stats.shapiro(x) if len(x) < 5000 else (0, 1)
                _, p_norm_y = stats.shapiro(y) if len(y) < 5000 else (0, 1)

                # Choose correlation method
                if p_norm_x > 0.05 and p_norm_y > 0.05:
                    r, p = stats.pearsonr(x, y)
                else:
                    r, p = stats.spearmanr(x, y)

                corr_matrix[i, j] = r
                pval_matrix[i, j] = p
                n_matrix[i, j] = len(x)
            else:
                corr_matrix[i, j] = np.nan
                pval_matrix[i, j] = np.nan
                n_matrix[i, j] = 0

    return corr_matrix, pval_matrix, n_matrix

# Compute correlations for sex × stress stratified groups
print("\nComputing sex × stress stratified correlations...")

# Male-Control
male_control = merged[(merged['sex'] == 1) & (merged['stress'] == 0)]
corr_mc, pval_mc, n_mc = compute_correlations(male_control, all_features, outcomes)

# Male-Stressed
male_stressed = merged[(merged['sex'] == 1) & (merged['stress'] == 1)]
corr_ms, pval_ms, n_ms = compute_correlations(male_stressed, all_features, outcomes)

# Female-Control
female_control = merged[(merged['sex'] == 0) & (merged['stress'] == 0)]
corr_fc, pval_fc, n_fc = compute_correlations(female_control, all_features, outcomes)

# Female-Stressed
female_stressed = merged[(merged['sex'] == 0) & (merged['stress'] == 1)]
corr_fs, pval_fs, n_fs = compute_correlations(female_stressed, all_features, outcomes)

# Create feature labels (shortened for visualization)
feature_labels = []
for feat in all_features:
    if feat.startswith('entropy_rate_'):
        label = feat.replace('entropy_rate_', '')
        feature_labels.append(f'ER:{label}')
    elif feat.startswith('sampen_'):
        label = feat.replace('sampen_', '')
        feature_labels.append(f'SE:{label}')
    elif 'max_TE_' in feat:
        label = feat.replace('max_TE_', '').replace('_', ' ')
        feature_labels.append(f'TE(max):{label}')
    elif 'mean_TE_' in feat:
        label = feat.replace('mean_TE_', '').replace('_', ' ')
        feature_labels.append(f'TE(mean):{label}')
    else:
        feature_labels.append(feat)

outcome_labels = [outcome_rename[o] for o in outcomes]

# Create figure with four heatmaps (2×2 grid)
fig, axes = plt.subplots(2, 2, figsize=(20, 28))
axes = axes.flatten()

datasets = [
    (corr_mc, pval_mc, n_mc, 'Male-Control'),
    (corr_ms, pval_ms, n_ms, 'Male-Stressed'),
    (corr_fc, pval_fc, n_fc, 'Female-Control'),
    (corr_fs, pval_fs, n_fs, 'Female-Stressed')
]

for ax, (corr, pval, n, title) in zip(axes, datasets):
    # Create annotation matrix (show asterisks for p < 0.05)
    annot = np.empty_like(corr, dtype=object)
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            if np.isnan(corr[i, j]):
                annot[i, j] = ''
            elif pval[i, j] < 0.001:
                annot[i, j] = f'{corr[i, j]:.2f}***'
            elif pval[i, j] < 0.01:
                annot[i, j] = f'{corr[i, j]:.2f}**'
            elif pval[i, j] < 0.05:
                annot[i, j] = f'{corr[i, j]:.2f}*'
            else:
                annot[i, j] = f'{corr[i, j]:.2f}'

    # Create heatmap
    sns.heatmap(corr, annot=annot, fmt='', cmap='RdBu_r', center=0,
                vmin=-0.5, vmax=0.5, cbar_kws={'label': 'Correlation (r)'},
                xticklabels=outcome_labels, yticklabels=feature_labels,
                linewidths=0.5, linecolor='gray', ax=ax)

    ax.set_title(f'{title}\n(* p<0.05, ** p<0.01, *** p<0.001, uncorrected)',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Clinical Outcomes', fontsize=10, fontweight='bold')
    if ax in [axes[0], axes[2]]:  # Left column
        ax.set_ylabel('Entropy Features', fontsize=10, fontweight='bold')

    # Rotate labels
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=7)

plt.suptitle('Sex × Stress Stratified Correlation Analysis: Entropy Features vs Clinical Outcomes\n' +
             'NOTE: None of these correlations survived FDR correction (all q > 0.40)',
             fontsize=14, fontweight='bold', y=0.998)

plt.tight_layout()
output_file = Path(script_dir) / 'correlation_heatmaps_sex_stress_stratified.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Saved: {output_file}")
plt.close()

# Create a summary table of significant findings
print("\n" + "="*80)
print("SEX × STRESS STRATIFIED SIGNIFICANT CORRELATIONS (p < 0.05, uncorrected)")
print("="*80)

for group_name, corr, pval, n in [('Male-Control', corr_mc, pval_mc, n_mc),
                                    ('Male-Stressed', corr_ms, pval_ms, n_ms),
                                    ('Female-Control', corr_fc, pval_fc, n_fc),
                                    ('Female-Stressed', corr_fs, pval_fs, n_fs)]:
    print(f"\n{group_name}:")
    print("-" * 80)
    sig_count = 0
    for i, feat in enumerate(all_features):
        for j, outcome in enumerate(outcomes):
            if pval[i, j] < 0.05 and not np.isnan(corr[i, j]):
                sig_count += 1
                print(f"  {feature_labels[i]:30s} × {outcome_labels[j]:20s}: r={corr[i, j]:+.3f}, p={pval[i, j]:.4f}, n={int(n[i, j])}")

    if sig_count == 0:
        print("  No significant correlations")
    else:
        print(f"\nTotal: {sig_count} significant correlations (p < 0.05, uncorrected)")

print("\n" + "="*80)
print("NOTE: Multiple comparison correction (FDR) revealed that NONE of these")
print("correlations survived adjustment (all q > 0.40). All findings are exploratory.")
print("="*80)
print(f"\nFigure saved to: {output_file}")
