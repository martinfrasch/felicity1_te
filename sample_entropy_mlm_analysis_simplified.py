#!/usr/bin/env python3
"""
Sample Entropy MLM Analysis - SIMPLIFIED VERSION
Due to extreme sparsity in conditioned SampEn data, this version:
- Focuses on conditioning levels with sufficient data (none, mother_accel, mother_decel)
- Uses simpler model without all interaction terms
- Tests key question: Does SampEn show bivariate coupling like entropy rate?

Model: Value ~ Sex + Stress + HR_Source + Conditioning + HR_Source:Conditioning + (1|Patient_ID)

Data quality issues:
- fetus_decel: 0/120 (0.0%) - EXCLUDED
- fetus_accel: 8/120 (6.7%) - EXCLUDED (too sparse)
- mother_accel: 16/120 (13.3%) - INCLUDED
- mother_decel: 7/120 (5.8%) - INCLUDED (marginal but critical for comparison)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.regression.mixed_linear_model import MixedLM
import sys

# Redirect output to file
output_file = open('sample_entropy_mlm_results_simplified.txt', 'w')
sys.stdout = output_file

print("=" * 80)
print("SAMPLE ENTROPY MLM ANALYSIS - SIMPLIFIED")
print("Conditioning Framework with Data Quality Constraints")
print("=" * 80)
print()

# ============================================================================
# LOAD DATA
# ============================================================================

print("Loading sample entropy data...")

# Load SampEn.txt
sampen_df = pd.read_csv('SampEn.txt', sep=r'\s+', header=None)
sampen_df.columns = [
    'patient_id',
    'fetus_full',
    'mother_full',
    'fetus_fHR_accel',
    'mother_fHR_accel',
    'fetus_fHR_decel',
    'mother_fHR_decel',
    'fetus_mHR_accel',
    'mother_mHR_accel',
    'fetus_mHR_decel',
    'mother_mHR_decel'
]

print(f"Loaded {len(sampen_df)} patients")
print()

# Data quality check
print("Data Quality Assessment:")
print("-" * 80)
for col in sampen_df.columns[1:]:
    non_zero = (sampen_df[col] > 0).sum()
    pct = 100 * non_zero / len(sampen_df)
    print(f"{col:25s}: {non_zero:3d}/{len(sampen_df)} ({pct:5.1f}%)")
print()

# Load sex/stress information from TE files
te_file = 'Nicolas_felicity1/max_TE_mHR_conditioning.csv'
print(f"Loading sex/stress information from {te_file}...")
te_df = pd.read_csv(te_file, sep=r'\s+', header=None)
te_df.columns = ['patient_id', 'sex', 'stress', 'all', 'accel', 'decel']

# Create sex/stress mapping
sex_stress_map = {}
for idx, row in te_df.iterrows():
    patient_id = int(row['patient_id'])
    sex_stress_map[patient_id] = {
        'Sex': 'male' if row['sex'] == 1 else 'female',
        'Stress': 'stressed' if row['stress'] == 1 else 'control'
    }

print(f"Loaded sex/stress for {len(sex_stress_map)} patients")
print()

# ============================================================================
# RESHAPE TO LONG FORMAT - SIMPLIFIED
# ============================================================================

print("Reshaping to long format (simplified conditioning)...")
print()

# Create long-format data - ONLY INCLUDING SUFFICIENT DATA CONDITIONING TYPES
records = []

for idx, row in sampen_df.iterrows():
    patient_id = int(row['patient_id'])

    if patient_id not in sex_stress_map:
        continue

    sex = sex_stress_map[patient_id]['Sex']
    stress = sex_stress_map[patient_id]['Stress']

    # Univariate baseline (no conditioning)
    if row['fetus_full'] > 0:
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'fetal',
            'Conditioning': 'none',
            'Value': row['fetus_full']
        })

    if row['mother_full'] > 0:
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'maternal',
            'Conditioning': 'none',
            'Value': row['mother_full']
        })

    # Cross-conditioned: maternal events (bivariate coupling test)
    # mother_accel: 16/120 (13.3%)
    if row['fetus_mHR_accel'] > 0:
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'fetal',
            'Conditioning': 'mother_accel',
            'Value': row['fetus_mHR_accel']
        })

    if row['mother_mHR_accel'] > 0:
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'maternal',
            'Conditioning': 'mother_accel',
            'Value': row['mother_mHR_accel']
        })

    # mother_decel: 7/120 (5.8%) - sparse but critical for comparison
    if row['fetus_mHR_decel'] > 0:
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'fetal',
            'Conditioning': 'mother_decel',
            'Value': row['fetus_mHR_decel']
        })

    if row['mother_mHR_decel'] > 0:
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'maternal',
            'Conditioning': 'mother_decel',
            'Value': row['mother_mHR_decel']
        })

df = pd.DataFrame(records)

print(f"Created long-format dataframe:")
print(f"  Total observations: {len(df)}")
print(f"  Unique patients: {df['Patient_ID'].nunique()}")
print(f"  Observations per patient: {len(df) / df['Patient_ID'].nunique():.1f}")
print()

print("Distributions:")
for col in ['Sex', 'Stress', 'HR_Source', 'Conditioning']:
    print(f"  {col}: {df[col].value_counts().to_dict()}")
print()

print("Sample entropy value statistics:")
print(f"  Mean: {df['Value'].mean():.4f}")
print(f"  Std: {df['Value'].std():.4f}")
print(f"  Min: {df['Value'].min():.4f}")
print(f"  Max: {df['Value'].max():.4f}")
print()

# Save data
df.to_csv('sample_entropy_mlm_data_simplified.csv', index=False)
print("✓ Saved data to: sample_entropy_mlm_data_simplified.csv")
print()

# ============================================================================
# FIT MLM MODEL - SIMPLIFIED
# ============================================================================

print("=" * 80)
print("MIXED LINEAR MODEL: SAMPLE ENTROPY (SIMPLIFIED)")
print("=" * 80)
print()

print("Model specification:")
print("  Value ~ Sex + Stress + HR_Source + Conditioning + HR_Source:Conditioning + (1|Patient_ID)")
print("  (Simplified due to sparse conditioned data)")
print(f"  N observations: {len(df)}")
print(f"  N patients: {df['Patient_ID'].nunique()}")
print()

# Define formula - SIMPLIFIED (fewer interactions)
formula = """Value ~ C(Sex) + C(Stress) + C(HR_Source) + C(Conditioning) +
                    C(HR_Source):C(Conditioning)"""

# Fit model
print("Fitting model with REML estimation...")
try:
    model = MixedLM.from_formula(formula, data=df, groups=df["Patient_ID"], re_formula="1")
    result = model.fit(reml=True, method='lbfgs')

    print()
    print("=" * 80)
    print("MODEL RESULTS: SAMPLE ENTROPY")
    print("=" * 80)
    print()
    print(result.summary())
    print()

    # ============================================================================
    # EXTRACT AND SORT RESULTS
    # ============================================================================

    print("=" * 80)
    print("SIGNIFICANT EFFECTS (sorted by p-value)")
    print("=" * 80)
    print()

    # Extract coefficients
    params = result.params
    pvalues = result.pvalues
    stderr = result.bse

    # Create results dataframe
    results_list = []
    for param in params.index:
        if param == 'Group Var':
            continue

        coef = params[param]
        p = pvalues[param]
        se = stderr[param]

        # Significance markers
        if p < 0.001:
            sig = '***'
        elif p < 0.01:
            sig = '**'
        elif p < 0.05:
            sig = '*'
        elif p < 0.10:
            sig = '†'
        else:
            sig = 'ns'

        # Clean parameter name
        param_clean = param.replace('C(', '').replace(')', '').replace('[T.', '(').replace(']', ')')

        results_list.append({
            'Parameter': param_clean,
            'Coef': coef,
            'SE': se,
            'p-value': p,
            'Sig': sig
        })

    results_df = pd.DataFrame(results_list)
    results_df = results_df.sort_values('p-value')

    # Print sorted results
    print(results_df.to_string(index=False))
    print()

    # Save results
    results_df.to_csv('sample_entropy_mlm_results_simplified.csv', index=False)
    print("✓ Saved to: sample_entropy_mlm_results_simplified.csv")
    print()

    # ============================================================================
    # KEY FINDINGS
    # ============================================================================

    print("=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    print()

    # Conditioning effects
    print("CONDITIONING EFFECTS (testing bivariate coupling in SampEn):")
    print()
    cond_effects = results_df[results_df['Parameter'].str.contains('Conditioning')]
    for idx, row in cond_effects.iterrows():
        print(f"{row['Parameter']:50s}: β = {row['Coef']:7.4f}, p = {row['p-value']:.6f} {row['Sig']}")
    print()

    # Demographic effects
    print("DEMOGRAPHIC EFFECTS:")
    print()
    demo_effects = results_df[results_df['Parameter'].str.contains('Sex|Stress')]
    demo_effects = demo_effects[~demo_effects['Parameter'].str.contains('Conditioning')]
    for idx, row in demo_effects.iterrows():
        print(f"{row['Parameter']:50s}: β = {row['Coef']:7.4f}, p = {row['p-value']:.6f} {row['Sig']}")
    print()

    # HR Source effects
    print("HR SOURCE EFFECTS:")
    print()
    hr_effects = results_df[results_df['Parameter'].str.contains('HR_Source')]
    hr_effects = hr_effects[~hr_effects['Parameter'].str.contains('Conditioning')]
    for idx, row in hr_effects.iterrows():
        print(f"{row['Parameter']:50s}: β = {row['Coef']:7.4f}, p = {row['p-value']:.6f} {row['Sig']}")
    print()

    # ============================================================================
    # COMPARISON WITH ENTROPY RATE
    # ============================================================================

    print("=" * 80)
    print("COMPARISON: SAMPLE ENTROPY vs ENTROPY RATE (HMAX/HMEAN)")
    print("=" * 80)
    print()

    print("ENTROPY RATE (hmax/hmean) conditioning effects:")
    print("  - Conditioning(none): β = +0.206, p < 0.001***")
    print("  - Conditioning(mother_decel): β = -0.123, p = 0.012*")
    print("  - Coupling strength: 60% reduction (0.123/0.206)")
    print()

    print("SAMPLE ENTROPY conditioning effects (from this simplified analysis):")
    sig_cond = cond_effects[cond_effects['p-value'] < 0.10]
    if len(sig_cond) > 0:
        for idx, row in sig_cond.iterrows():
            print(f"  - {row['Parameter']}: β = {row['Coef']:+.4f}, p = {row['p-value']:.3f} {row['Sig']}")

        # Calculate coupling strength if baseline effect exists
        baseline_effects = cond_effects[cond_effects['Parameter'].str.contains('none')]
        mother_decel_effects = cond_effects[cond_effects['Parameter'].str.contains('mother_decel')]

        if len(baseline_effects) > 0 and len(mother_decel_effects) > 0:
            baseline_coef = baseline_effects.iloc[0]['Coef']
            decel_coef = mother_decel_effects.iloc[0]['Coef']
            if baseline_coef != 0:
                coupling_pct = abs(decel_coef / baseline_coef) * 100
                print(f"  - Coupling strength estimate: {coupling_pct:.0f}% reduction")
    else:
        print("  - No significant conditioning effects detected at p < 0.10")
    print()

    print("=" * 80)
    print("DATA QUALITY LIMITATIONS")
    print("=" * 80)
    print()
    print("Sparse conditioned data in SampEn.txt:")
    print("  - Excluded: fetus_decel (0/120, 0.0%)")
    print("  - Excluded: fetus_accel (8/120, 6.7%)")
    print("  - Included: mother_accel (16/120, 13.3%)")
    print("  - Included: mother_decel (7/120, 5.8%)")
    print()
    print("Comparison to entropy rate data:")
    print("  - Entropy rate had ~1,262 observations with complete conditioning")
    print("  - Sample entropy has only 286 observations with limited conditioning types")
    print()
    print("Interpretation: Sample entropy is harder to compute reliably in short")
    print("event windows (accelerations/decelerations), resulting in extensive zeros.")
    print("This limits our ability to detect bivariate coupling signatures that may")
    print("exist but cannot be measured with current data sparsity.")
    print()

except Exception as e:
    print(f"ERROR: Model fitting failed: {e}")
    print()
    print("This may indicate:")
    print("  - Still too sparse data for model complexity")
    print("  - Need further simplification")
    print("  - Or data quality issues preventing convergence")

# Close output file
sys.stdout = sys.__stdout__
output_file.close()

print("Analysis complete!")
print("Results saved to: sample_entropy_mlm_results_simplified.txt")
print("Data saved to: sample_entropy_mlm_data_simplified.csv")
print("Results table saved to: sample_entropy_mlm_results_simplified.csv")
