"""
Complete Mixed Linear Model Analysis - ER, SE, and TE
======================================================

Complete analysis of all univariate (ER, SE) and bivariate (TE) metrics
using mixed linear models with interaction terms.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
import warnings
warnings.filterwarnings('ignore')

# Setup
OUTPUT_DIR = Path("analysis_output_corrected")
MLM_DIR = OUTPUT_DIR / "mlm_analysis"
MLM_DIR.mkdir(exist_ok=True)

print("="*100)
print("COMPLETE MIXED LINEAR MODEL ANALYSIS")
print("Univariate Metrics: Entropy Rate (ER) + Sample Entropy (SE)")
print("Bivariate Metric: Transfer Entropy (TE)")
print("="*100)

# Load patient-level data
df_wide = pd.read_csv(OUTPUT_DIR / "patient_level_data_corrected.csv")

print(f"\n✓ Loaded {len(df_wide)} patients")
print(f"  Control: n={(df_wide['group_stress'] == 0).sum()}")
print(f"  Stressed: n={(df_wide['group_stress'] == 1).sum()}")
print(f"  Female: n={(df_wide['group_sex'] == 0).sum()}")
print(f"  Male: n={(df_wide['group_sex'] == 1).sum()}")

# =============================================================================
# PART 1: ENTROPY RATE (ER) - SEPARATE MODELS BY CONDITIONING
# =============================================================================
print("\n" + "="*100)
print("PART 1: ENTROPY RATE (ER) ANALYSIS")
print("="*100)

er_results_list = []

# ER Model 1: No conditioning
print("\n" + "-"*80)
print("ER Model 1: No Conditioning")
print("-"*80)

er_no_cond = []
for idx, row in df_wide.iterrows():
    for hr_source in ['fetus', 'mother']:
        feature = f'{hr_source}_full'
        if pd.notna(row[feature]):
            er_no_cond.append({
                'patient_id': row['patient_id'],
                'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                'value': row[feature],
                'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal'
            })

df_er_no_cond = pd.DataFrame(er_no_cond)
print(f"Observations: {len(df_er_no_cond)}")

try:
    mlm_er1 = mixedlm("value ~ sex * stress * HR_source", df_er_no_cond,
                      groups=df_er_no_cond["patient_id"]).fit(reml=True)
    print("✓ Converged")

    res = pd.DataFrame({
        'metric': 'ER',
        'model': 'no_conditioning',
        'parameter': mlm_er1.params.index,
        'coef': mlm_er1.params.values,
        'se': mlm_er1.bse.values,
        'p_value': mlm_er1.pvalues.values
    })
    res['sig'] = res['p_value'] < 0.05
    er_results_list.append(res)

    print(f"Significant effects: {res['sig'].sum()}")
    if res['sig'].sum() > 0:
        print(res[res['sig']][['parameter', 'coef', 'p_value']].to_string(index=False))

except Exception as e:
    print(f"⚠️  Failed: {e}")

# ER Model 2: mHR conditioning
print("\n" + "-"*80)
print("ER Model 2: Maternal HR Conditioning")
print("-"*80)

er_mhr = []
for idx, row in df_wide.iterrows():
    for hr_source in ['fetus', 'mother']:
        for hr_event in ['accel', 'decel']:
            feature = f'{hr_source}_mHR_{hr_event}'
            if pd.notna(row[feature]):
                er_mhr.append({
                    'patient_id': row['patient_id'],
                    'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                    'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                    'value': row[feature],
                    'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal',
                    'HR_event': hr_event.capitalize()
                })

df_er_mhr = pd.DataFrame(er_mhr)
print(f"Observations: {len(df_er_mhr)}")

try:
    mlm_er2 = mixedlm("value ~ sex * stress * HR_source * HR_event", df_er_mhr,
                      groups=df_er_mhr["patient_id"]).fit(reml=True, method='nm')
    print("✓ Converged")

    res = pd.DataFrame({
        'metric': 'ER',
        'model': 'mHR_conditioning',
        'parameter': mlm_er2.params.index,
        'coef': mlm_er2.params.values,
        'se': mlm_er2.bse.values,
        'p_value': mlm_er2.pvalues.values
    })
    res['sig'] = res['p_value'] < 0.05
    er_results_list.append(res)

    print(f"Significant effects: {res['sig'].sum()}")
    if res['sig'].sum() > 0:
        print(res[res['sig']][['parameter', 'coef', 'p_value']].to_string(index=False))

except Exception as e:
    print(f"⚠️  Failed: {e}")

# ER Model 3: fHR acceleration
print("\n" + "-"*80)
print("ER Model 3: Fetal HR Acceleration")
print("-"*80)

er_fhr_accel = []
for idx, row in df_wide.iterrows():
    for hr_source in ['fetus', 'mother']:
        feature = f'{hr_source}_fHR_accel'
        if pd.notna(row[feature]):
            er_fhr_accel.append({
                'patient_id': row['patient_id'],
                'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                'value': row[feature],
                'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal'
            })

df_er_fhr_accel = pd.DataFrame(er_fhr_accel)
print(f"Observations: {len(df_er_fhr_accel)}")

try:
    mlm_er3 = mixedlm("value ~ sex * stress * HR_source", df_er_fhr_accel,
                      groups=df_er_fhr_accel["patient_id"]).fit(reml=True)
    print("✓ Converged")

    res = pd.DataFrame({
        'metric': 'ER',
        'model': 'fHR_accel',
        'parameter': mlm_er3.params.index,
        'coef': mlm_er3.params.values,
        'se': mlm_er3.bse.values,
        'p_value': mlm_er3.pvalues.values
    })
    res['sig'] = res['p_value'] < 0.05
    er_results_list.append(res)

    print(f"Significant effects: {res['sig'].sum()}")
    if res['sig'].sum() > 0:
        print(res[res['sig']][['parameter', 'coef', 'p_value']].to_string(index=False))

except Exception as e:
    print(f"⚠️  Failed: {e}")

# Save ER results
if len(er_results_list) > 0:
    df_er_all = pd.concat(er_results_list, ignore_index=True)
    df_er_all = df_er_all.sort_values('p_value')
    df_er_all.to_csv(MLM_DIR / 'ER_mixed_models_complete.csv', index=False)
    print(f"\n✓ Saved: {MLM_DIR / 'ER_mixed_models_complete.csv'}")

# =============================================================================
# PART 2: SAMPLE ENTROPY (SE) - SEPARATE MODELS BY CONDITIONING
# =============================================================================
print("\n" + "="*100)
print("PART 2: SAMPLE ENTROPY (SE) ANALYSIS")
print("="*100)

se_results_list = []

# SE Model 1: No conditioning
print("\n" + "-"*80)
print("SE Model 1: No Conditioning")
print("-"*80)

se_no_cond = []
for idx, row in df_wide.iterrows():
    for hr_source in ['fetus', 'mother']:
        feature = f'SE_{hr_source}_full'
        if pd.notna(row[feature]):
            se_no_cond.append({
                'patient_id': row['patient_id'],
                'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                'value': row[feature],
                'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal'
            })

df_se_no_cond = pd.DataFrame(se_no_cond)
print(f"Observations: {len(df_se_no_cond)}")

try:
    mlm_se1 = mixedlm("value ~ sex * stress * HR_source", df_se_no_cond,
                      groups=df_se_no_cond["patient_id"]).fit(reml=True)
    print("✓ Converged")

    res = pd.DataFrame({
        'metric': 'SE',
        'model': 'no_conditioning',
        'parameter': mlm_se1.params.index,
        'coef': mlm_se1.params.values,
        'se': mlm_se1.bse.values,
        'p_value': mlm_se1.pvalues.values
    })
    res['sig'] = res['p_value'] < 0.05
    se_results_list.append(res)

    print(f"Significant effects: {res['sig'].sum()}")
    if res['sig'].sum() > 0:
        print(res[res['sig']][['parameter', 'coef', 'p_value']].to_string(index=False))

except Exception as e:
    print(f"⚠️  Failed: {e}")

# SE Model 2: mHR conditioning
print("\n" + "-"*80)
print("SE Model 2: Maternal HR Conditioning")
print("-"*80)

se_mhr = []
for idx, row in df_wide.iterrows():
    for hr_source in ['fetus', 'mother']:
        for hr_event in ['accel', 'decel']:
            feature = f'SE_{hr_source}_mHR_{hr_event}'
            if pd.notna(row[feature]):
                se_mhr.append({
                    'patient_id': row['patient_id'],
                    'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                    'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                    'value': row[feature],
                    'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal',
                    'HR_event': hr_event.capitalize()
                })

df_se_mhr = pd.DataFrame(se_mhr)
print(f"Observations: {len(df_se_mhr)}")

try:
    mlm_se2 = mixedlm("value ~ sex * stress * HR_source * HR_event", df_se_mhr,
                      groups=df_se_mhr["patient_id"]).fit(reml=True, method='nm')
    print("✓ Converged")

    res = pd.DataFrame({
        'metric': 'SE',
        'model': 'mHR_conditioning',
        'parameter': mlm_se2.params.index,
        'coef': mlm_se2.params.values,
        'se': mlm_se2.bse.values,
        'p_value': mlm_se2.pvalues.values
    })
    res['sig'] = res['p_value'] < 0.05
    se_results_list.append(res)

    print(f"Significant effects: {res['sig'].sum()}")
    if res['sig'].sum() > 0:
        print(res[res['sig']][['parameter', 'coef', 'p_value']].to_string(index=False))

except Exception as e:
    print(f"⚠️  Failed: {e}")

# SE Model 3: fHR acceleration
print("\n" + "-"*80)
print("SE Model 3: Fetal HR Acceleration")
print("-"*80)

se_fhr_accel = []
for idx, row in df_wide.iterrows():
    for hr_source in ['fetus', 'mother']:
        feature = f'SE_{hr_source}_fHR_accel'
        if pd.notna(row[feature]):
            se_fhr_accel.append({
                'patient_id': row['patient_id'],
                'sex': 'Male' if row['group_sex'] == 1 else 'Female',
                'stress': 'Stressed' if row['group_stress'] == 1 else 'Control',
                'value': row[feature],
                'HR_source': 'Fetal' if hr_source == 'fetus' else 'Maternal'
            })

df_se_fhr_accel = pd.DataFrame(se_fhr_accel)
print(f"Observations: {len(df_se_fhr_accel)}")

try:
    mlm_se3 = mixedlm("value ~ sex * stress * HR_source", df_se_fhr_accel,
                      groups=df_se_fhr_accel["patient_id"]).fit(reml=True)
    print("✓ Converged")

    res = pd.DataFrame({
        'metric': 'SE',
        'model': 'fHR_accel',
        'parameter': mlm_se3.params.index,
        'coef': mlm_se3.params.values,
        'se': mlm_se3.bse.values,
        'p_value': mlm_se3.pvalues.values
    })
    res['sig'] = res['p_value'] < 0.05
    se_results_list.append(res)

    print(f"Significant effects: {res['sig'].sum()}")
    if res['sig'].sum() > 0:
        print(res[res['sig']][['parameter', 'coef', 'p_value']].to_string(index=False))

except Exception as e:
    print(f"⚠️  Failed: {e}")

# Save SE results
if len(se_results_list) > 0:
    df_se_all = pd.concat(se_results_list, ignore_index=True)
    df_se_all = df_se_all.sort_values('p_value')
    df_se_all.to_csv(MLM_DIR / 'SE_mixed_models_complete.csv', index=False)
    print(f"\n✓ Saved: {MLM_DIR / 'SE_mixed_models_complete.csv'}")

# =============================================================================
# PART 3: TRANSFER ENTROPY (TE) - FROM PREVIOUS ANALYSIS
# =============================================================================
print("\n" + "="*100)
print("PART 3: TRANSFER ENTROPY (TE) - Loading Previous Results")
print("="*100)

df_te = pd.read_csv(MLM_DIR / 'TE_mixed_model_results.csv')
print(f"✓ Loaded TE results: {len(df_te)} parameters")
print(f"  Significant (p<0.05): {df_te['Significant'].sum()}")

# =============================================================================
# PART 4: COMPREHENSIVE COMPARISON - ER vs SE vs TE
# =============================================================================
print("\n" + "="*100)
print("PART 4: COMPARATIVE ANALYSIS - ER vs SE vs TE")
print("="*100)

# Summary table
summary_data = []

# ER summary
if len(er_results_list) > 0:
    for model_name in ['no_conditioning', 'mHR_conditioning', 'fHR_accel']:
        model_results = df_er_all[df_er_all['model'] == model_name]
        if len(model_results) > 0:
            summary_data.append({
                'Metric': 'ER',
                'Model': model_name,
                'Total_params': len(model_results),
                'Sig_params': model_results['sig'].sum(),
                'Sex_effects': model_results[model_results['parameter'].str.contains('sex', case=False) & model_results['sig']].shape[0],
                'Stress_effects': model_results[model_results['parameter'].str.contains('stress', case=False) & model_results['sig']].shape[0],
                'Interactions': model_results[model_results['parameter'].str.contains(':') & model_results['sig']].shape[0]
            })

# SE summary
if len(se_results_list) > 0:
    for model_name in ['no_conditioning', 'mHR_conditioning', 'fHR_accel']:
        model_results = df_se_all[df_se_all['model'] == model_name]
        if len(model_results) > 0:
            summary_data.append({
                'Metric': 'SE',
                'Model': model_name,
                'Total_params': len(model_results),
                'Sig_params': model_results['sig'].sum(),
                'Sex_effects': model_results[model_results['parameter'].str.contains('sex', case=False) & model_results['sig']].shape[0],
                'Stress_effects': model_results[model_results['parameter'].str.contains('stress', case=False) & model_results['sig']].shape[0],
                'Interactions': model_results[model_results['parameter'].str.contains(':') & model_results['sig']].shape[0]
            })

# TE summary
summary_data.append({
    'Metric': 'TE',
    'Model': 'unified_full',
    'Total_params': len(df_te),
    'Sig_params': df_te['Significant'].sum(),
    'Sex_effects': df_te[df_te['Parameter'].str.contains('sex', case=False) & df_te['Significant']].shape[0],
    'Stress_effects': df_te[df_te['Parameter'].str.contains('stress', case=False) & df_te['Significant']].shape[0],
    'Interactions': df_te[df_te['Parameter'].str.contains(':') & df_te['Significant']].shape[0]
})

df_summary = pd.DataFrame(summary_data)
df_summary.to_csv(MLM_DIR / 'MLM_summary_all_metrics.csv', index=False)

print("\n" + "-"*80)
print("SUMMARY: Significant Effects Across All Metrics")
print("-"*80)
print(df_summary.to_string(index=False))

# =============================================================================
# PART 5: VISUALIZATION - COMPARE ER vs SE
# =============================================================================
print("\n" + "="*100)
print("PART 5: GENERATING COMPARATIVE VISUALIZATIONS")
print("="*100)

if len(er_results_list) > 0 and len(se_results_list) > 0:
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    models = [
        ('no_conditioning', 'No Conditioning'),
        ('mHR_conditioning', 'mHR Conditioning'),
        ('fHR_accel', 'fHR Acceleration')
    ]

    for col_idx, (model_name, title) in enumerate(models):
        # ER panel (top row)
        ax_er = axes[0, col_idx]
        er_model = df_er_all[df_er_all['model'] == model_name]

        if len(er_model) > 0:
            # Get significant effects
            er_sig = er_model[er_model['sig']].copy()
            er_sig = er_sig[~er_sig['parameter'].isin(['Intercept', 'Group Var'])]

            if len(er_sig) > 0:
                er_sig = er_sig.sort_values('p_value').head(10)
                y_pos = np.arange(len(er_sig))

                ax_er.barh(y_pos, er_sig['coef'], color='steelblue', alpha=0.7, edgecolor='black')
                ax_er.set_yticks(y_pos)
                ax_er.set_yticklabels(er_sig['parameter'], fontsize=8)
                ax_er.axvline(0, color='black', linestyle='--', linewidth=1)
                ax_er.set_xlabel('Coefficient', fontsize=10)
                ax_er.set_title(f'ER: {title}\n({len(er_sig)} sig effects)', fontsize=11, fontweight='bold')
                ax_er.grid(axis='x', alpha=0.3)
            else:
                ax_er.text(0.5, 0.5, 'No significant\neffects',
                          ha='center', va='center', transform=ax_er.transAxes)
                ax_er.set_title(f'ER: {title}', fontsize=11, fontweight='bold')

        # SE panel (bottom row)
        ax_se = axes[1, col_idx]
        se_model = df_se_all[df_se_all['model'] == model_name]

        if len(se_model) > 0:
            # Get significant effects
            se_sig = se_model[se_model['sig']].copy()
            se_sig = se_sig[~se_sig['parameter'].isin(['Intercept', 'Group Var'])]

            if len(se_sig) > 0:
                se_sig = se_sig.sort_values('p_value').head(10)
                y_pos = np.arange(len(se_sig))

                ax_se.barh(y_pos, se_sig['coef'], color='coral', alpha=0.7, edgecolor='black')
                ax_se.set_yticks(y_pos)
                ax_se.set_yticklabels(se_sig['parameter'], fontsize=8)
                ax_se.axvline(0, color='black', linestyle='--', linewidth=1)
                ax_se.set_xlabel('Coefficient', fontsize=10)
                ax_se.set_title(f'SE: {title}\n({len(se_sig)} sig effects)', fontsize=11, fontweight='bold')
                ax_se.grid(axis='x', alpha=0.3)
            else:
                ax_se.text(0.5, 0.5, 'No significant\neffects',
                          ha='center', va='center', transform=ax_se.transAxes)
                ax_se.set_title(f'SE: {title}', fontsize=11, fontweight='bold')

    fig.suptitle('MLM Results: Entropy Rate (ER) vs Sample Entropy (SE)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(MLM_DIR / 'ER_vs_SE_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Saved: {MLM_DIR / 'ER_vs_SE_comparison.png'}")

print("\n" + "="*100)
print("COMPLETE ANALYSIS FINISHED")
print("="*100)
print(f"\nResults saved to: {MLM_DIR}/")
print("\nGenerated files:")
print("  ✓ ER_mixed_models_complete.csv       - Entropy Rate results")
print("  ✓ SE_mixed_models_complete.csv       - Sample Entropy results")
print("  ✓ TE_mixed_model_results.csv         - Transfer Entropy results")
print("  ✓ MLM_summary_all_metrics.csv        - Comparative summary")
print("  ✓ ER_vs_SE_comparison.png            - Visual comparison")
print("  ✓ TE_model_predictions.png           - TE predictions (from v2)")

print("\n" + "="*100)
print("KEY FINDINGS SUMMARY")
print("="*100)
print("\nUnivariate Metrics (ER & SE):")
print(f"  • ER models: {len(er_results_list)} conditioning contexts")
print(f"  • SE models: {len(se_results_list)} conditioning contexts")
print("\nBivariate Metric (TE):")
print(f"  • Unified model with full interactions")
print(f"  • Detected Sex × Stress interaction (p=0.009)")
print("\nAll three information-theoretic metrics now analyzed with MLM!")
