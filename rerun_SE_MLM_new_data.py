"""
Re-run Sample Entropy MLM with Nicolas's recomputed SampEn data.
The new data resolves the data quality limitation (old: 87-100% zeros; new: ~99.5% non-zero).
"""

import numpy as np
import pandas as pd
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

# Load patient-level data for group labels
df_wide = pd.read_csv("../analysis_output_corrected/patient_level_data_corrected.csv")
print(f"Patient CSV: {len(df_wide)} patients")

# Load new SampEn data
SAMPEN_DIR = "SampEn_new"

# Build mapping from numpy index to patient_id
# The numpy arrays have 120 entries for 'all' group
# We need to match these to the 119 patients in df_wide
# First, let's check the group sizes
test = np.load(f"{SAMPEN_DIR}/SampEnmax_fetus_no_conditoning.npz")
print(f"\nNew SampEn 'all' array size: {len(test['all'])}")
print(f"stressed: {len(test['stressed'])}, control: {len(test['control'])}")
print(f"male: {len(test['male'])}, female: {len(test['female'])}")

# Check group sizes in df_wide
print(f"\ndf_wide groups:")
print(f"  stress=1 (stressed): {(df_wide['group_stress']==1).sum()}")
print(f"  stress=0 (control): {(df_wide['group_stress']==0).sum()}")
print(f"  sex=1 (male): {(df_wide['group_sex']==1).sum()}")
print(f"  sex=0 (female): {(df_wide['group_sex']==0).sum()}")

# Note: numpy has 120 patients, CSV has 119. We'll work with numpy arrays directly.
# Build long-format data from numpy arrays using the 'all' group

# Define conditioning structure
conditions = {
    'no_conditioning': 'no_conditoning',  # note: typo in filenames
    'mother_accel': 'mother_accel',
    'mother_decel': 'mother_decel',
    'fetus_accel': 'fetus_accel',
    'fetus_decel': 'fetus_decel',
}

hr_sources = ['fetus', 'mother']
metrics = ['SampEnmax', 'SampEnmean']

# Load stressed/control/male/female arrays to identify group membership
ref = np.load(f"{SAMPEN_DIR}/SampEnmax_fetus_no_conditoning.npz")
all_vals = ref['all']
stressed_vals = ref['stressed']
control_vals = ref['control']
male_vals = ref['male']
female_vals = ref['female']

n_all = len(all_vals)
n_stressed = len(stressed_vals)
n_control = len(control_vals)
n_male = len(male_vals)
n_female = len(female_vals)

print(f"\nGroup sizes: all={n_all}, stressed={n_stressed}, control={n_control}, male={n_male}, female={n_female}")

# Build long-format DataFrame
records = []
patient_counter = 0

for metric in metrics:
    for hr_source in hr_sources:
        for cond_name, cond_file in conditions.items():
            fname = f"{SAMPEN_DIR}/{metric}_{hr_source}_{cond_file}.npz"
            data = np.load(fname)
            arr = data['all']

            for i, val in enumerate(arr):
                if val != 0:  # Only include non-zero values
                    records.append({
                        'patient_id': f'P{i:03d}',
                        'value': val,
                        'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal',
                        'conditioning': cond_name,
                        'metric': 'SEmax' if 'max' in metric else 'SEmean',
                    })

df_long = pd.DataFrame(records)
print(f"\nTotal non-zero observations: {len(df_long)}")
print(f"Observations per patient: {len(df_long)/n_all:.1f}")

# Add group info using subgroup arrays
# Match patients to stressed/control using the subgroup arrays
# Strategy: compare values in 'all' array to 'stressed' and 'control' arrays
ref_no_cond = np.load(f"{SAMPEN_DIR}/SampEnmax_fetus_no_conditoning.npz")
all_v = ref_no_cond['all']
stressed_v = ref_no_cond['stressed']
control_v = ref_no_cond['control']
male_v = ref_no_cond['male']
female_v = ref_no_cond['female']

# Build stress and sex labels
stress_labels = {}
sex_labels = {}

# For stress: match all values to stressed/control subgroup values
stressed_set = set(stressed_v.tolist())
control_set = set(control_v.tolist())
male_set = set(male_v.tolist())
female_set = set(female_v.tolist())

# Simple matching: count stressed index, control index
s_idx = 0
c_idx = 0
m_idx = 0
f_idx = 0

for i in range(n_all):
    pid = f'P{i:03d}'
    # Match stress group
    if s_idx < n_stressed and all_v[i] == stressed_v[s_idx]:
        stress_labels[pid] = 'Stressed'
        s_idx += 1
    elif c_idx < n_control and all_v[i] == control_v[c_idx]:
        stress_labels[pid] = 'Control'
        c_idx += 1
    else:
        stress_labels[pid] = 'Unknown'

    # Match sex group
    if m_idx < n_male and all_v[i] == male_v[m_idx]:
        sex_labels[pid] = 'Male'
        m_idx += 1
    elif f_idx < n_female and all_v[i] == female_v[f_idx]:
        sex_labels[pid] = 'Female'
        f_idx += 1
    else:
        sex_labels[pid] = 'Unknown'

df_long['stress'] = df_long['patient_id'].map(stress_labels)
df_long['sex'] = df_long['patient_id'].map(sex_labels)

print(f"\nStress classification: {df_long['stress'].value_counts().to_dict()}")
print(f"Sex classification: {df_long['sex'].value_counts().to_dict()}")

# Check for unknowns
n_unknown_stress = (df_long['stress'] == 'Unknown').sum()
n_unknown_sex = (df_long['sex'] == 'Unknown').sum()
if n_unknown_stress > 0 or n_unknown_sex > 0:
    print(f"WARNING: {n_unknown_stress} unknown stress, {n_unknown_sex} unknown sex")

# =====================================================================
# Run SE MLM - Full model (matching ER MLM structure)
# =====================================================================
print("\n" + "="*80)
print("SAMPLE ENTROPY MLM - NEW DATA")
print("="*80)

# Filter to known groups only
df_mlm = df_long[
    (df_long['stress'] != 'Unknown') &
    (df_long['sex'] != 'Unknown')
].copy()
print(f"\nMLM dataset: {len(df_mlm)} observations, {df_mlm['patient_id'].nunique()} patients")

# Model 1: Full model matching ER structure
print("\n--- Model 1: Full model (all conditioning) ---")
formula1 = "value ~ sex * stress * metric * HR_source * conditioning"
try:
    model1 = mixedlm(formula1, df_mlm, groups=df_mlm["patient_id"]).fit(reml=True)
    print("Converged!")
    res1 = pd.DataFrame({
        'parameter': model1.params.index,
        'coef': model1.params.values,
        'se': model1.bse.values,
        'p_value': model1.pvalues.values,
    })
    sig = res1[res1['p_value'] < 0.05]
    print(f"\nSignificant effects ({len(sig)}):")
    for _, row in sig.iterrows():
        stars = '***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*'
        print(f"  {row['parameter']}: β={row['coef']:.4f}, SE={row['se']:.4f}, p={row['p_value']:.4f} {stars}")
except Exception as e:
    print(f"Full model failed: {e}")
    print("Trying simplified model...")

# Model 2: Simplified (matching original ER MLM focus)
print("\n--- Model 2: Key effects model ---")
formula2 = "value ~ sex * stress + metric + HR_source * conditioning"
try:
    model2 = mixedlm(formula2, df_mlm, groups=df_mlm["patient_id"]).fit(reml=True)
    print("Converged!")
    res2 = pd.DataFrame({
        'parameter': model2.params.index,
        'coef': model2.params.values,
        'se': model2.bse.values,
        'p_value': model2.pvalues.values,
    })
    print(f"\nAll effects:")
    for _, row in res2.iterrows():
        sig_str = '***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*' if row['p_value'] < 0.05 else '†' if row['p_value'] < 0.10 else 'ns'
        print(f"  {row['parameter']}: β={row['coef']:.4f}, SE={row['se']:.4f}, p={row['p_value']:.4f} {sig_str}")
except Exception as e:
    print(f"Simplified model failed: {e}")

# Model 3: Conditioning-focused (most comparable to ER result)
print("\n--- Model 3: Conditioning-focused (comparable to ER MLM) ---")
formula3 = "value ~ sex + stress + metric + HR_source + conditioning + HR_source:conditioning"
try:
    model3 = mixedlm(formula3, df_mlm, groups=df_mlm["patient_id"]).fit(reml=True)
    print("Converged!")
    res3 = pd.DataFrame({
        'parameter': model3.params.index,
        'coef': model3.params.values,
        'se': model3.bse.values,
        'p_value': model3.pvalues.values,
    })
    print(f"\nAll effects:")
    for _, row in res3.iterrows():
        sig_str = '***' if row['p_value'] < 0.001 else '**' if row['p_value'] < 0.01 else '*' if row['p_value'] < 0.05 else '†' if row['p_value'] < 0.10 else 'ns'
        print(f"  {row['parameter']}: β={row['coef']:.4f}, SE={row['se']:.4f}, p={row['p_value']:.4f} {sig_str}")

    # Key comparison with ER results
    print("\n--- Key comparison: SE vs ER coupling signatures ---")
    for _, row in res3.iterrows():
        if 'conditioning' in row['parameter'].lower() or 'Conditioning' in row['parameter']:
            print(f"  {row['parameter']}: β={row['coef']:.4f}, p={row['p_value']:.4f}")

except Exception as e:
    print(f"Conditioning model failed: {e}")

# Summary statistics
print("\n" + "="*80)
print("DATA QUALITY COMPARISON: OLD vs NEW")
print("="*80)
print(f"{'Metric':<30} {'Old SE':<20} {'New SE':<20} {'ER':<20}")
print("-"*90)
n_obs = len(df_mlm)
n_pat = df_mlm['patient_id'].nunique()
obs_per_pat = n_obs / n_pat
print(f"{'Total observations':<30} {'286':<20} {str(n_obs):<20} {'1,262':<20}")
print(f"{'Obs per patient':<30} {'2.4':<20} {f'{obs_per_pat:.1f}':<20} {'10.5':<20}")
print(f"{'Non-zero rate':<30} {'13-23%':<20} {'~99.5%':<20} {'~100%':<20}")
