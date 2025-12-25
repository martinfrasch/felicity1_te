"""
Data Validation Script
Check integrity of .npz data files
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats

DATA_DIR = Path("/Users/mfrasch/Library/CloudStorage/GoogleDrive-mg@frasch.ca/My Drive/Cloud work/Nicolas Garnier/FELICITy1_TE_paper/TE_ER_data")

print("DATA VALIDATION REPORT")
print("="*100)

results = []

for filepath in sorted(DATA_DIR.glob("*.npz")):
    data = np.load(filepath)

    record = {'file': filepath.name}

    # Check each group
    for key in ['all', 'stressed', 'control', 'male', 'female']:
        if key in data.files:
            arr = data[key]
            record[f'{key}_n'] = len(arr)
            record[f'{key}_mean'] = np.nanmean(arr)
            record[f'{key}_std'] = np.nanstd(arr)
            record[f'{key}_nan_count'] = np.sum(np.isnan(arr))
        else:
            record[f'{key}_n'] = 0
            record[f'{key}_mean'] = np.nan
            record[f'{key}_std'] = np.nan
            record[f'{key}_nan_count'] = np.nan

    # Check if stressed and control are identical
    if 'stressed' in data.files and 'control' in data.files:
        stressed = data['stressed']
        control = data['control']

        # Remove NaNs for comparison
        stressed_clean = stressed[~np.isnan(stressed)]
        control_clean = control[~np.isnan(control)]

        if len(stressed_clean) > 0 and len(control_clean) > 0:
            identical = np.array_equal(stressed, control)
            record['stressed_control_identical'] = identical

            if not identical:
                t_stat, p_val = stats.ttest_ind(stressed_clean, control_clean)
                cohens_d = (np.mean(stressed_clean) - np.mean(control_clean)) / np.sqrt((np.var(stressed_clean) + np.var(control_clean)) / 2)
                record['exposure_tstat'] = t_stat
                record['exposure_pval'] = p_val
                record['exposure_cohens_d'] = cohens_d
            else:
                record['exposure_tstat'] = 0
                record['exposure_pval'] = 1.0
                record['exposure_cohens_d'] = 0
        else:
            record['stressed_control_identical'] = 'insufficient_data'

    # Check if male and female are different
    if 'male' in data.files and 'female' in data.files:
        male = data['male']
        female = data['female']

        male_clean = male[~np.isnan(male)]
        female_clean = female[~np.isnan(female)]

        if len(male_clean) > 0 and len(female_clean) > 0:
            t_stat, p_val = stats.ttest_ind(male_clean, female_clean)
            cohens_d = (np.mean(male_clean) - np.mean(female_clean)) / np.sqrt((np.var(male_clean) + np.var(female_clean)) / 2)
            record['sex_tstat'] = t_stat
            record['sex_pval'] = p_val
            record['sex_cohens_d'] = cohens_d

    results.append(record)

# Create dataframe
df = pd.DataFrame(results)

# Print summary
print("\nSample Sizes:")
print(df[['file', 'all_n', 'stressed_n', 'control_n', 'male_n', 'female_n']].to_string(index=False))

print("\n" + "="*100)
print("\nFiles with Identical Stressed/Control Data:")
identical_files = df[df['stressed_control_identical'] == True]['file'].tolist()
if identical_files:
    for f in identical_files:
        print(f"  - {f}")
else:
    print("  None found")

print("\n" + "="*100)
print("\nStatistically Significant Effects (p < 0.05):")

# Exposure effects
sig_exposure = df[df['exposure_pval'] < 0.05].sort_values('exposure_pval')
if len(sig_exposure) > 0:
    print("\nEXPOSURE EFFECTS:")
    print(sig_exposure[['file', 'stressed_mean', 'control_mean', 'exposure_tstat', 'exposure_pval', 'exposure_cohens_d']].to_string(index=False))
else:
    print("\nEXPOSURE EFFECTS: None")

# Sex effects
sig_sex = df[df['sex_pval'] < 0.05].sort_values('sex_pval')
if len(sig_sex) > 0:
    print("\nSEX EFFECTS:")
    print(sig_sex[['file', 'male_mean', 'female_mean', 'sex_tstat', 'sex_pval', 'sex_cohens_d']].to_string(index=False))
else:
    print("\nSEX EFFECTS: None")

# Save validation report
OUTPUT_DIR = Path("/Users/mfrasch/Library/CloudStorage/GoogleDrive-mg@frasch.ca/My Drive/Cloud work/Nicolas Garnier/FELICITy1_TE_paper/analysis_output")
df.to_csv(OUTPUT_DIR / 'data_validation_report.csv', index=False)
print(f"\n\nValidation report saved to: {OUTPUT_DIR / 'data_validation_report.csv'}")
