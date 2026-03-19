"""
Sensitivity Analysis: Covariate Adjustment for Reviewer Response
================================================================

Two-part strategy:
Part 1: Add gestational age and maternal age as covariates (reviewer explicitly requested)
Part 2: Add BMI as continuous covariate (significant group difference, p=.009)

Re-runs the primary mixed linear models from mixed_linear_model_analysis_complete.py
with covariates added, and compares results to the original (unadjusted) models.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

# Setup
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "analysis_output_corrected"
SENS_DIR = Path(__file__).parent / "sensitivity_analysis_output"
SENS_DIR.mkdir(exist_ok=True)

print("=" * 100)
print("SENSITIVITY ANALYSIS: COVARIATE ADJUSTMENT")
print("=" * 100)

# Load entropy/TE data
df_wide = pd.read_csv(OUTPUT_DIR / "patient_level_data_corrected.csv")

# Load clinical data and merge covariates
clinical = pd.read_excel(Path(__file__).parent / 'FELICITy-Dataset-MixedModels.ods', engine='odf')

# Build covariate lookup from clinical data
cov_data = clinical[['PATIENT_CODE', 'ante__Alter_bei_Studieneintritt',
                      'ante__BMI_preagest', 'ante__Gestationsalter_bei_Geburt_1']].copy()
cov_data.columns = ['Patient', 'maternal_age', 'bmi', 'ga_birth']

# Merge covariates using the string Patient column
df_wide = df_wide.merge(cov_data, left_on='Patient', right_on='Patient', how='left')

print(f"\nLoaded {len(df_wide)} patients")
print(f"  Covariate availability:")
print(f"    Maternal age: {df_wide['maternal_age'].notna().sum()}")
print(f"    Pre-gest BMI: {df_wide['bmi'].notna().sum()}")
print(f"    GA at birth:  {df_wide['ga_birth'].notna().sum()}")

# Standardize continuous covariates for model stability
for col in ['maternal_age', 'bmi', 'ga_birth']:
    vals = df_wide[col]
    df_wide[f'{col}_z'] = (vals - vals.mean()) / vals.std()


# =============================================================================
# Helper functions
# =============================================================================

def build_long_format(df_wide, features, hr_sources, hr_events=None, extra_cols=None):
    """Build long-format data from wide patient data."""
    records = []
    for idx, row in df_wide.iterrows():
        if hr_events:
            for hr_source in hr_sources:
                for hr_event in hr_events:
                    feature = features(hr_source, hr_event)
                    if pd.notna(row.get(feature, np.nan)):
                        rec = {
                            'patient_id': row['patient_id'],
                            'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                            'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                            'value': row[feature],
                            'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal',
                            'HR_event': hr_event.capitalize(),
                        }
                        if extra_cols:
                            for c in extra_cols:
                                rec[c] = row[c]
                        records.append(rec)
        else:
            for hr_source in hr_sources:
                feature = features(hr_source)
                if pd.notna(row.get(feature, np.nan)):
                    rec = {
                        'patient_id': row['patient_id'],
                        'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                        'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                        'value': row[feature],
                        'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal',
                    }
                    if extra_cols:
                        for c in extra_cols:
                            rec[c] = row[c]
                    records.append(rec)
    return pd.DataFrame(records)


def run_model(formula, df, groups_col='patient_id', method='reml_default'):
    """Fit a mixed linear model, return results DataFrame."""
    try:
        if method == 'nm':
            model = mixedlm(formula, df, groups=df[groups_col]).fit(reml=True, method='nm')
        else:
            model = mixedlm(formula, df, groups=df[groups_col]).fit(reml=True)
        return pd.DataFrame({
            'parameter': model.params.index,
            'coef': model.params.values,
            'se': model.bse.values,
            'p_value': model.pvalues.values
        })
    except Exception as e:
        print(f"    ⚠ Model failed: {e}")
        return None


def compare_models(orig, adj, label):
    """Compare original vs adjusted model results."""
    if orig is None or adj is None:
        return None
    merged = orig.merge(adj, on='parameter', suffixes=('_orig', '_adj'))
    merged['coef_change_pct'] = 100 * (merged['coef_adj'] - merged['coef_orig']) / merged['coef_orig'].abs()
    merged['sig_orig'] = merged['p_value_orig'] < 0.05
    merged['sig_adj'] = merged['p_value_adj'] < 0.05
    merged['sig_changed'] = merged['sig_orig'] != merged['sig_adj']
    merged['model'] = label
    return merged


# Covariate sets
COVARIATES = {
    'Part1_GA_Age': 'ga_birth_z + maternal_age_z',
    'Part2_GA_Age_BMI': 'ga_birth_z + maternal_age_z + bmi_z',
}

extra_cols = ['maternal_age_z', 'bmi_z', 'ga_birth_z']

all_comparisons = []

# =============================================================================
# ENTROPY RATE MODELS
# =============================================================================
print("\n" + "=" * 100)
print("ENTROPY RATE (ER) SENSITIVITY ANALYSIS")
print("=" * 100)

# --- ER Model 1: No conditioning ---
print("\n--- ER Model 1: No Conditioning ---")
df_long = build_long_format(
    df_wide,
    features=lambda src, *a: f'{src}_full',
    hr_sources=['fetus', 'mother'],
    extra_cols=extra_cols
)
df_long_complete = df_long.dropna(subset=['maternal_age_z', 'ga_birth_z', 'bmi_z'])
print(f"  Observations: {len(df_long)} (complete cases: {len(df_long_complete)})")

base_formula = "value ~ sex * stress * HR_source"
orig = run_model(base_formula, df_long_complete)

for cov_name, cov_formula in COVARIATES.items():
    adj_formula = f"value ~ sex * stress * HR_source + {cov_formula}"
    print(f"  {cov_name}: {adj_formula}")
    adj = run_model(adj_formula, df_long_complete)
    comp = compare_models(orig, adj, f"ER_no_cond_{cov_name}")
    if comp is not None:
        all_comparisons.append(comp)

# --- ER Model 2: mHR conditioning ---
print("\n--- ER Model 2: Maternal HR Conditioning ---")
df_long = build_long_format(
    df_wide,
    features=lambda src, evt: f'{src}_mHR_{evt}',
    hr_sources=['fetus', 'mother'],
    hr_events=['accel', 'decel'],
    extra_cols=extra_cols
)
df_long_complete = df_long.dropna(subset=['maternal_age_z', 'ga_birth_z', 'bmi_z'])
print(f"  Observations: {len(df_long)} (complete cases: {len(df_long_complete)})")

base_formula = "value ~ sex * stress * HR_source * HR_event"
orig = run_model(base_formula, df_long_complete, method='nm')

for cov_name, cov_formula in COVARIATES.items():
    adj_formula = f"value ~ sex * stress * HR_source * HR_event + {cov_formula}"
    print(f"  {cov_name}: {adj_formula}")
    adj = run_model(adj_formula, df_long_complete, method='nm')
    comp = compare_models(orig, adj, f"ER_mHR_cond_{cov_name}")
    if comp is not None:
        all_comparisons.append(comp)

# --- ER Model 3: fHR acceleration ---
print("\n--- ER Model 3: Fetal HR Acceleration ---")
df_long = build_long_format(
    df_wide,
    features=lambda src, *a: f'{src}_fHR_accel',
    hr_sources=['fetus', 'mother'],
    extra_cols=extra_cols
)
df_long_complete = df_long.dropna(subset=['maternal_age_z', 'ga_birth_z', 'bmi_z'])
print(f"  Observations: {len(df_long)} (complete cases: {len(df_long_complete)})")

base_formula = "value ~ sex * stress * HR_source"
orig = run_model(base_formula, df_long_complete)

for cov_name, cov_formula in COVARIATES.items():
    adj_formula = f"value ~ sex * stress * HR_source + {cov_formula}"
    print(f"  {cov_name}: {adj_formula}")
    adj = run_model(adj_formula, df_long_complete)
    comp = compare_models(orig, adj, f"ER_fHR_accel_{cov_name}")
    if comp is not None:
        all_comparisons.append(comp)

# =============================================================================
# SAMPLE ENTROPY MODELS
# =============================================================================
print("\n" + "=" * 100)
print("SAMPLE ENTROPY (SE) SENSITIVITY ANALYSIS")
print("=" * 100)

# --- SE Model 1: No conditioning ---
print("\n--- SE Model 1: No Conditioning ---")
df_long = build_long_format(
    df_wide,
    features=lambda src, *a: f'SE_{src}_full',
    hr_sources=['fetus', 'mother'],
    extra_cols=extra_cols
)
df_long_complete = df_long.dropna(subset=['maternal_age_z', 'ga_birth_z', 'bmi_z', 'value'])
print(f"  Observations: {len(df_long)} (complete cases: {len(df_long_complete)})")

base_formula = "value ~ sex * stress * HR_source"
orig = run_model(base_formula, df_long_complete)

for cov_name, cov_formula in COVARIATES.items():
    adj_formula = f"value ~ sex * stress * HR_source + {cov_formula}"
    print(f"  {cov_name}: {adj_formula}")
    adj = run_model(adj_formula, df_long_complete)
    comp = compare_models(orig, adj, f"SE_no_cond_{cov_name}")
    if comp is not None:
        all_comparisons.append(comp)

# --- SE Model 2: mHR conditioning ---
print("\n--- SE Model 2: Maternal HR Conditioning ---")
df_long = build_long_format(
    df_wide,
    features=lambda src, evt: f'SE_{src}_mHR_{evt}',
    hr_sources=['fetus', 'mother'],
    hr_events=['accel', 'decel'],
    extra_cols=extra_cols
)
df_long_complete = df_long.dropna(subset=['maternal_age_z', 'ga_birth_z', 'bmi_z', 'value'])
print(f"  Observations: {len(df_long)} (complete cases: {len(df_long_complete)})")

if len(df_long_complete) > 20:
    base_formula = "value ~ sex * stress * HR_source * HR_event"
    orig = run_model(base_formula, df_long_complete, method='nm')

    for cov_name, cov_formula in COVARIATES.items():
        adj_formula = f"value ~ sex * stress * HR_source * HR_event + {cov_formula}"
        print(f"  {cov_name}: {adj_formula}")
        adj = run_model(adj_formula, df_long_complete, method='nm')
        comp = compare_models(orig, adj, f"SE_mHR_cond_{cov_name}")
        if comp is not None:
            all_comparisons.append(comp)
else:
    print("  Skipped: insufficient non-zero observations")

# =============================================================================
# TRANSFER ENTROPY MODEL
# =============================================================================
print("\n" + "=" * 100)
print("TRANSFER ENTROPY (TE) SENSITIVITY ANALYSIS")
print("=" * 100)

# Build TE long format from the max/mean TE columns
te_records = []
te_cols = {
    'max_TE_fHR_all': ('max', 'fHR', 'none'),
    'max_TE_fHR_accel': ('max', 'fHR', 'accel'),
    'max_TE_fHR_decel': ('max', 'fHR', 'decel'),
    'max_TE_mHR_all': ('max', 'mHR', 'none'),
    'max_TE_mHR_accel': ('max', 'mHR', 'accel'),
    'max_TE_mHR_decel': ('max', 'mHR', 'decel'),
    'mean_TE_fHR_all': ('mean', 'fHR', 'none'),
    'mean_TE_fHR_accel': ('mean', 'fHR', 'accel'),
    'mean_TE_fHR_decel': ('mean', 'fHR', 'decel'),
    'mean_TE_mHR_all': ('mean', 'mHR', 'none'),
    'mean_TE_mHR_accel': ('mean', 'mHR', 'accel'),
    'mean_TE_mHR_decel': ('mean', 'mHR', 'decel'),
}

for idx, row in df_wide.iterrows():
    for col, (te_type, hr_source, conditioning) in te_cols.items():
        val = row.get(col, np.nan)
        if pd.notna(val):
            te_records.append({
                'patient_id': row['patient_id'],
                'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                'TE_value': val,
                'TE_type': te_type,
                'HR_source': hr_source,
                'conditioning': conditioning,
                'maternal_age_z': row['maternal_age_z'],
                'bmi_z': row['bmi_z'],
                'ga_birth_z': row['ga_birth_z'],
            })

df_te = pd.DataFrame(te_records)
df_te_complete = df_te.dropna(subset=['maternal_age_z', 'ga_birth_z', 'bmi_z'])
print(f"  Observations: {len(df_te)} (complete cases: {len(df_te_complete)})")

base_formula = "TE_value ~ sex * stress * TE_type * HR_source * conditioning"
print(f"\n  Base formula: {base_formula}")
orig = run_model(base_formula, df_te_complete, method='nm')

for cov_name, cov_formula in COVARIATES.items():
    adj_formula = f"TE_value ~ sex * stress * TE_type * HR_source * conditioning + {cov_formula}"
    print(f"  {cov_name}: adjusting with + {cov_formula}")
    adj = run_model(adj_formula, df_te_complete, method='nm')
    comp = compare_models(orig, adj, f"TE_full_{cov_name}")
    if comp is not None:
        all_comparisons.append(comp)


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 100)
print("SUMMARY: SENSITIVITY ANALYSIS RESULTS")
print("=" * 100)

if all_comparisons:
    df_all = pd.concat(all_comparisons, ignore_index=True)
    df_all.to_csv(SENS_DIR / 'sensitivity_all_comparisons.csv', index=False)

    # Focus on key effects (those significant in original)
    sig_orig = df_all[df_all['sig_orig']].copy()

    print(f"\nTotal model-parameter comparisons: {len(df_all)}")
    print(f"Originally significant effects: {len(sig_orig)}")
    print(f"Effects that CHANGED significance after adjustment: {sig_orig['sig_changed'].sum()}")

    if sig_orig['sig_changed'].sum() > 0:
        print("\n⚠ EFFECTS THAT CHANGED SIGNIFICANCE:")
        changed = sig_orig[sig_orig['sig_changed']]
        print(changed[['model', 'parameter', 'p_value_orig', 'p_value_adj',
                       'coef_orig', 'coef_adj', 'coef_change_pct']].to_string(index=False))
    else:
        print("\n✓ NO originally significant effects changed significance after covariate adjustment.")

    # Summary table of key interaction effects
    key_params = sig_orig[sig_orig['parameter'].str.contains('stress|sex', case=False)]
    if len(key_params) > 0:
        print(f"\n--- Key stress/sex effects (originally significant) ---")
        for _, row in key_params.iterrows():
            direction = "→ remained sig" if row['sig_adj'] else "→ LOST significance"
            print(f"  {row['model']:40s} | {row['parameter']:45s} | "
                  f"p_orig={row['p_value_orig']:.4f} p_adj={row['p_value_adj']:.4f} | "
                  f"Δcoef={row['coef_change_pct']:+.1f}% {direction}")

    # Covariate effects summary
    cov_params = df_all[df_all['parameter'].isin(['ga_birth_z', 'maternal_age_z', 'bmi_z'])]
    if len(cov_params) > 0:
        print(f"\n--- Covariate effects (are covariates themselves significant?) ---")
        for _, row in cov_params.iterrows():
            sig_marker = "*" if row['p_value_adj'] < 0.05 else "ns"
            print(f"  {row['model']:40s} | {row['parameter']:15s} | "
                  f"coef={row['coef_adj']:+.4f} p={row['p_value_adj']:.4f} {sig_marker}")

    print(f"\n✓ Full results saved to: {SENS_DIR / 'sensitivity_all_comparisons.csv'}")

    # Generate LaTeX summary table
    print("\n--- LaTeX summary for manuscript ---")
    summary_rows = []
    for model_name in df_all['model'].unique():
        model_data = df_all[df_all['model'] == model_name]
        n_sig_orig = model_data['sig_orig'].sum()
        n_changed = model_data[model_data['sig_orig']]['sig_changed'].sum()
        max_coef_change = model_data[model_data['sig_orig']]['coef_change_pct'].abs().max()
        summary_rows.append({
            'Model': model_name,
            'N_sig_original': n_sig_orig,
            'N_changed': n_changed,
            'Max_coef_change_pct': max_coef_change
        })

    df_summary = pd.DataFrame(summary_rows)
    df_summary.to_csv(SENS_DIR / 'sensitivity_summary.csv', index=False)
    print(df_summary.to_string(index=False))

else:
    print("\n⚠ No comparisons were successfully completed.")

print("\n" + "=" * 100)
print("SENSITIVITY ANALYSIS COMPLETE")
print("=" * 100)
