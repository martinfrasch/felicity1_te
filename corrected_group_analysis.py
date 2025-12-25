"""
Corrected Group Analysis Using Excel as Ground Truth
Compares stressed vs control and male vs female using correct group assignments
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
from statsmodels.stats import multitest

# Paths
EXCEL_FILE = Path("groups_scores_new.xlsx")
NICOLAS_DIR = Path("Nicolas_felicity1")
OUTPUT_DIR = Path("analysis_output_corrected")
OUTPUT_DIR.mkdir(exist_ok=True)

print("="*100)
print("CORRECTED GROUP ANALYSIS")
print("Using groups_scores_new.xlsx as ground truth for group assignments")
print("="*100)

# Step 1: Load Excel file (ground truth)
print("\nStep 1: Loading Excel file (ground truth)...")
df_excel = pd.read_excel(EXCEL_FILE)
print(f"  Excel: {len(df_excel)} patients")
print(f"  Group 0 (Control): {(df_excel['Group'] == 0).sum()}")
print(f"  Group 1 (Stressed): {(df_excel['Group'] == 1).sum()}")

# Step 2: Load entropy_rate.txt
print("\nStep 2: Loading entropy_rate.txt...")
er_data = []
with open(NICOLAS_DIR / "entropy_rate.txt", 'r') as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            patient_id = int(parts[0])
            values = [float(v) if v != 'nan' else np.nan for v in parts[1:]]
            er_data.append([patient_id] + values)

er_columns = ['patient_id', 'fetus_full', 'mother_full',
              'fetus_fHR_accel', 'mother_fHR_accel',
              'fetus_fHR_decel', 'mother_fHR_decel',
              'fetus_mHR_accel', 'mother_mHR_accel',
              'fetus_mHR_decel', 'mother_mHR_decel']
df_er = pd.DataFrame(er_data, columns=er_columns)
print(f"  Entropy Rate: {len(df_er)} patients, 10 features")

# Step 3: Load SampEn.txt
print("\nStep 3: Loading SampEn.txt...")
se_data = []
with open(NICOLAS_DIR / "SampEn.txt", 'r') as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            patient_id = int(parts[0])
            values = [float(v) if v != 'nan' else np.nan for v in parts[1:]]
            se_data.append([patient_id] + values)

se_columns = ['patient_id', 'SE_fetus_full', 'SE_mother_full',
              'SE_fetus_fHR_accel', 'SE_mother_fHR_accel',
              'SE_fetus_fHR_decel', 'SE_mother_fHR_decel',
              'SE_fetus_mHR_accel', 'SE_mother_mHR_accel',
              'SE_fetus_mHR_decel', 'SE_mother_mHR_decel']
df_se = pd.DataFrame(se_data, columns=se_columns)
print(f"  Sample Entropy: {len(df_se)} patients, 10 features")

# Step 4: Load TE CSV files
print("\nStep 4: Loading TE CSV files...")
te_files = {
    'max_TE_fHR': NICOLAS_DIR / "max_TE_fHR_conditioning.csv",
    'max_TE_mHR': NICOLAS_DIR / "max_TE_mHR_conditioning.csv",
    'mean_TE_fHR': NICOLAS_DIR / "mean_TE_fHR_conditioning.csv",
    'mean_TE_mHR': NICOLAS_DIR / "mean_TE_mHR_conditioning.csv"
}

te_dfs = {}
for key, filepath in te_files.items():
    df = pd.read_csv(filepath, sep=r'\s+', header=None,
                     names=['patient_id', 'sex_csv', 'stress_csv', 'all', 'accel', 'decel'])
    te_dfs[key] = df
    print(f"  {key}: {len(df)} patients")

# Combine all TE data
df_te = te_dfs['max_TE_fHR'][['patient_id', 'sex_csv', 'stress_csv']].copy()
for key, df in te_dfs.items():
    df_te[f'{key}_all'] = df['all'].values
    df_te[f'{key}_accel'] = df['accel'].values
    df_te[f'{key}_decel'] = df['decel'].values

print(f"\n  Combined TE: {len(df_te)} patients, 12 TE features")

# Step 5: Match patients to Excel and get correct groups
print("\nStep 5: Matching patients to Excel file...")

# Create patient ID mapping (numeric to FS-XXX format)
df_er['Patient'] = df_er['patient_id'].apply(lambda x: f'FS-{x:03d}')
df_se['Patient'] = df_se['patient_id'].apply(lambda x: f'FS-{x:03d}')
df_te['Patient'] = df_te['patient_id'].apply(lambda x: f'FS-{x:03d}')

# Merge with Excel to get correct groups
df_combined = df_er.merge(df_se, on=['patient_id', 'Patient'], how='inner')
df_combined = df_combined.merge(df_te, on=['patient_id', 'Patient'], how='inner')
df_combined = df_combined.merge(df_excel[['Patient', 'Group']], on='Patient', how='left')

print(f"  Matched patients: {df_combined['Group'].notna().sum()}/{len(df_combined)}")

# Check for mismatches between CSV groups and Excel groups
print("\nStep 6: Checking for group mismatches...")
df_matched = df_combined[df_combined['Group'].notna()].copy()

# Compare stress groups
stress_csv_from_excel = df_matched['stress_csv']
stress_excel = df_matched['Group']
mismatches_stress = (stress_csv_from_excel != stress_excel).sum()

print(f"  Stress group mismatches: {mismatches_stress}/{len(df_matched)}")
if mismatches_stress > 0:
    print(f"  WARNING: {mismatches_stress} patients have different stress assignments in CSV vs Excel!")
    mismatch_patients = df_matched[stress_csv_from_excel != stress_excel]['Patient'].tolist()
    print(f"  Mismatch patients: {mismatch_patients[:10]}{'...' if len(mismatch_patients) > 10 else ''}")

# For sex, we need to check if there's a sex column in Excel
# If not in Excel, we'll use the CSV values
print(f"\n  Using Excel groups as ground truth for stress/exposure")
print(f"  Using CSV values for sex (not in Excel)")

# Create final groups
df_matched['group_stress'] = df_matched['Group']  # 0=control, 1=stressed
df_matched['group_sex'] = df_matched['sex_csv']  # 0=female, 1=male

# Count final groups
print("\nFinal group counts (using Excel as ground truth):")
print(f"  Control (Group 0): {(df_matched['group_stress'] == 0).sum()}")
print(f"  Stressed (Group 1): {(df_matched['group_stress'] == 1).sum()}")
print(f"  Female (sex 0): {(df_matched['group_sex'] == 0).sum()}")
print(f"  Male (sex 1): {(df_matched['group_sex'] == 1).sum()}")
print(f"  Total matched: {len(df_matched)}")

# Step 7: Statistical Analysis
print("\n" + "="*100)
print("STATISTICAL ANALYSIS WITH CORRECTED GROUPS")
print("="*100)

def compare_groups(data, group1_mask, group2_mask, group1_name, group2_name, feature_name):
    """Compare two groups using independent samples t-test"""
    g1 = data[group1_mask]
    g2 = data[group2_mask]

    # Remove NaN values
    g1_clean = g1[~np.isnan(g1)]
    g2_clean = g2[~np.isnan(g2)]

    if len(g1_clean) < 2 or len(g2_clean) < 2:
        return None

    # T-test
    t_stat, p_value = stats.ttest_ind(g1_clean, g2_clean)

    # Cohen's d
    mean1 = np.mean(g1_clean)
    mean2 = np.mean(g2_clean)
    std1 = np.std(g1_clean, ddof=1)
    std2 = np.std(g2_clean, ddof=1)
    n1 = len(g1_clean)
    n2 = len(g2_clean)

    pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1 + n2 - 2))
    cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0

    # Mann-Whitney U (non-parametric)
    u_stat, mann_whitney_p = stats.mannwhitneyu(g1_clean, g2_clean, alternative='two-sided')

    return {
        'feature': feature_name,
        'n_group1': n1,
        'n_group2': n2,
        'mean_group1': mean1,
        'std_group1': std1,
        'mean_group2': mean2,
        'std_group2': std2,
        'tstat': t_stat,
        'pval': p_value,
        'cohens_d': cohens_d,
        'mann_whitney_p': mann_whitney_p,
        'group1_name': group1_name,
        'group2_name': group2_name
    }

# Define all features to analyze
er_features = [col for col in df_matched.columns if col.startswith(('fetus_', 'mother_')) and not col.startswith('SE_')]
se_features = [col for col in df_matched.columns if col.startswith('SE_')]
te_features = [col for col in df_matched.columns if col.startswith(('max_TE', 'mean_TE'))]

all_features = er_features + se_features + te_features

print(f"\nAnalyzing {len(all_features)} features:")
print(f"  Entropy Rate: {len(er_features)}")
print(f"  Sample Entropy: {len(se_features)}")
print(f"  Transfer Entropy: {len(te_features)}")

# Exposure effects (Stressed vs Control)
print("\n" + "="*100)
print("EXPOSURE EFFECTS (Stressed vs Control)")
print("="*100)

exposure_results = []
control_mask = df_matched['group_stress'] == 0
stressed_mask = df_matched['group_stress'] == 1

for feature in all_features:
    result = compare_groups(
        df_matched[feature].values,
        control_mask,
        stressed_mask,
        'Control',
        'Stressed',
        feature
    )
    if result:
        exposure_results.append(result)

df_exposure = pd.DataFrame(exposure_results)

# Apply multiple comparison corrections
df_exposure['p_bonferroni'] = df_exposure['pval'] * len(df_exposure)
df_exposure['p_bonferroni'] = df_exposure['p_bonferroni'].clip(upper=1.0)

reject_fdr, p_fdr, _, _ = multitest.multipletests(df_exposure['pval'], method='fdr_bh')
df_exposure['p_fdr'] = p_fdr
df_exposure['sig_fdr'] = reject_fdr

# Sort by p-value
df_exposure = df_exposure.sort_values('pval')

# Summary
print(f"\nResults:")
print(f"  Features analyzed: {len(df_exposure)}")
print(f"  Significant at p < 0.05 (uncorrected): {(df_exposure['pval'] < 0.05).sum()}")
print(f"  Significant after FDR correction: {df_exposure['sig_fdr'].sum()}")
print(f"  Median p-value: {df_exposure['pval'].median():.3f}")

if (df_exposure['pval'] < 0.05).sum() > 0:
    print(f"\nTop 10 most significant:")
    print(df_exposure[['feature', 'mean_group1', 'mean_group2', 'tstat', 'pval', 'cohens_d']].head(10).to_string(index=False))

# Save results
df_exposure.to_csv(OUTPUT_DIR / 'exposure_effects_corrected.csv', index=False)
print(f"\n✓ Saved: {OUTPUT_DIR / 'exposure_effects_corrected.csv'}")

# Sex effects (Male vs Female)
print("\n" + "="*100)
print("SEX EFFECTS (Male vs Female)")
print("="*100)

sex_results = []
female_mask = df_matched['group_sex'] == 0
male_mask = df_matched['group_sex'] == 1

for feature in all_features:
    result = compare_groups(
        df_matched[feature].values,
        male_mask,
        female_mask,
        'Male',
        'Female',
        feature
    )
    if result:
        sex_results.append(result)

df_sex = pd.DataFrame(sex_results)

# Apply multiple comparison corrections
df_sex['p_bonferroni'] = df_sex['pval'] * len(df_sex)
df_sex['p_bonferroni'] = df_sex['p_bonferroni'].clip(upper=1.0)

reject_fdr, p_fdr, _, _ = multitest.multipletests(df_sex['pval'], method='fdr_bh')
df_sex['p_fdr'] = p_fdr
df_sex['sig_fdr'] = reject_fdr

# Sort by p-value
df_sex = df_sex.sort_values('pval')

# Summary
print(f"\nResults:")
print(f"  Features analyzed: {len(df_sex)}")
print(f"  Significant at p < 0.05 (uncorrected): {(df_sex['pval'] < 0.05).sum()}")
print(f"  Significant after FDR correction: {df_sex['sig_fdr'].sum()}")
print(f"  Median p-value: {df_sex['pval'].median():.3f}")

if (df_sex['pval'] < 0.05).sum() > 0:
    print(f"\nTop 10 most significant:")
    print(df_sex[['feature', 'mean_group1', 'mean_group2', 'tstat', 'pval', 'cohens_d']].head(10).to_string(index=False))

# Save results
df_sex.to_csv(OUTPUT_DIR / 'sex_effects_corrected.csv', index=False)
print(f"\n✓ Saved: {OUTPUT_DIR / 'sex_effects_corrected.csv'}")

# Save combined dataset for further analysis
df_matched.to_csv(OUTPUT_DIR / 'patient_level_data_corrected.csv', index=False)
print(f"✓ Saved: {OUTPUT_DIR / 'patient_level_data_corrected.csv'}")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100)
print(f"\nOutput files saved to: {OUTPUT_DIR}/")
print(f"  - exposure_effects_corrected.csv")
print(f"  - sex_effects_corrected.csv")
print(f"  - patient_level_data_corrected.csv")
