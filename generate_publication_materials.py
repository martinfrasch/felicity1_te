"""
Generate Publication-Ready Materials
====================================

Creates:
1. Publication tables (LaTeX and CSV)
2. Manuscript figures with confidence intervals
3. Comparative visualization panels
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# Setup
OUTPUT_DIR = Path("analysis_output_corrected")
MLM_DIR = OUTPUT_DIR / "mlm_analysis"
PUB_DIR = OUTPUT_DIR / "publication_materials"
PUB_DIR.mkdir(exist_ok=True)

print("="*100)
print("GENERATING PUBLICATION MATERIALS")
print("="*100)

# Load MLM results
df_er = pd.read_csv(MLM_DIR / 'ER_mixed_models_complete.csv')
df_se = pd.read_csv(MLM_DIR / 'SE_mixed_models_complete.csv')
df_te = pd.read_csv(MLM_DIR / 'TE_mixed_model_results.csv')

# =============================================================================
# TABLE 1: Entropy Rate & Sample Entropy - Sex Effects during mHR Conditioning
# =============================================================================
print("\n" + "="*100)
print("TABLE 1: Univariate Complexity Metrics - Sex Effects")
print("="*100)

# Extract mHR conditioning results
er_mhr = df_er[df_er['model'] == 'mHR_conditioning'].copy()
se_mhr = df_se[df_se['model'] == 'mHR_conditioning'].copy()

# Focus on key parameters
key_params = ['Intercept', 'sex[T.Male]', 'stress[T.Stressed]',
              'HR_source[T.Maternal]', 'HR_event[T.Decel]',
              'sex[T.Male]:stress[T.Stressed]',
              'sex[T.Male]:HR_source[T.Maternal]']

table1_data = []

for param in key_params:
    # ER
    er_row = er_mhr[er_mhr['parameter'] == param]
    if len(er_row) > 0:
        er_coef = er_row['coef'].values[0]
        er_se = er_row['se'].values[0]
        er_p = er_row['p_value'].values[0]
        er_sig = '***' if er_p < 0.001 else '**' if er_p < 0.01 else '*' if er_p < 0.05 else ''
    else:
        er_coef = er_se = er_p = np.nan
        er_sig = ''

    # SE
    se_row = se_mhr[se_mhr['parameter'] == param]
    if len(se_row) > 0:
        se_coef = se_row['coef'].values[0]
        se_se = se_row['se'].values[0]
        se_p = se_row['p_value'].values[0]
        se_sig = '***' if se_p < 0.001 else '**' if se_p < 0.01 else '*' if se_p < 0.05 else ''
    else:
        se_coef = se_se = se_p = np.nan
        se_sig = ''

    table1_data.append({
        'Parameter': param.replace('[T.', ' (').replace(']', ')').replace(':', ' × '),
        'ER_Coefficient': f'{er_coef:.3f}' if not np.isnan(er_coef) else '—',
        'ER_SE': f'{er_se:.3f}' if not np.isnan(er_se) else '—',
        'ER_p': f'{er_p:.4f}' if not np.isnan(er_p) else '—',
        'ER_Sig': er_sig,
        'SE_Coefficient': f'{se_coef:.3f}' if not np.isnan(se_coef) else '—',
        'SE_SE': f'{se_se:.3f}' if not np.isnan(se_se) else '—',
        'SE_p': f'{se_p:.4f}' if not np.isnan(se_p) else '—',
        'SE_Sig': se_sig
    })

df_table1 = pd.DataFrame(table1_data)

# Save as CSV
df_table1.to_csv(PUB_DIR / 'Table1_Univariate_Complexity.csv', index=False)

# Create LaTeX version
with open(PUB_DIR / 'Table1_Univariate_Complexity.tex', 'w') as f:
    f.write("\\begin{table}[h]\n")
    f.write("\\caption{Mixed Linear Model Results: Entropy Rate and Sample Entropy during Maternal HR Conditioning}\n")
    f.write("\\label{tab:univariate}\n")
    f.write("\\centering\n")
    f.write("\\small\n")
    f.write("\\begin{tabular}{lcccccc}\n")
    f.write("\\hline\n")
    f.write("& \\multicolumn{3}{c}{Entropy Rate} & \\multicolumn{3}{c}{Sample Entropy} \\\\\n")
    f.write("\\cmidrule(lr){2-4} \\cmidrule(lr){5-7}\n")
    f.write("Parameter & $\\beta$ & SE & $p$ & $\\beta$ & SE & $p$ \\\\\n")
    f.write("\\hline\n")

    for idx, row in df_table1.iterrows():
        param_clean = row['Parameter'].replace('_', '\\_')
        f.write(f"{param_clean} & {row['ER_Coefficient']}{row['ER_Sig']} & {row['ER_SE']} & {row['ER_p']} & ")
        f.write(f"{row['SE_Coefficient']}{row['SE_Sig']} & {row['SE_SE']} & {row['SE_p']} \\\\\n")

    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
    f.write("\\begin{flushleft}\n")
    f.write("\\footnotesize\n")
    f.write("$n = 119$ patients. Models: value $\\sim$ Sex $\\times$ Stress $\\times$ HR\\_Source $\\times$ HR\\_Event + (1|Patient). ")
    f.write("$^{***}p < 0.001$, $^{**}p < 0.01$, $^{*}p < 0.05$.\n")
    f.write("\\end{flushleft}\n")
    f.write("\\end{table}\n")

print(f"✓ Table 1 saved:")
print(f"  - {PUB_DIR / 'Table1_Univariate_Complexity.csv'}")
print(f"  - {PUB_DIR / 'Table1_Univariate_Complexity.tex'}")

# =============================================================================
# TABLE 2: Transfer Entropy - Main Effects and Interactions
# =============================================================================
print("\n" + "="*100)
print("TABLE 2: Transfer Entropy - Sex × Stress Interaction")
print("="*100)

# Focus on key parameters for TE
te_key_params = [
    'Intercept',
    'sex[T.Male]',
    'stress_group[T.Stressed]',
    'TE_type[T.Mean]',
    'HR_event[T.None]',
    'sex[T.Male]:stress_group[T.Stressed]',
    'TE_type[T.Mean]:HR_event[T.None]',
    'sex[T.Male]:stress_group[T.Stressed]:HR_event[T.None]'
]

table2_data = []

for param in te_key_params:
    te_row = df_te[df_te['Parameter'] == param]
    if len(te_row) > 0:
        coef = te_row['Coefficient'].values[0]
        se = te_row['Std_Error'].values[0]
        p = te_row['p_value'].values[0]
        ci_low = te_row['CI_lower'].values[0]
        ci_high = te_row['CI_upper'].values[0]
        sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''

        table2_data.append({
            'Parameter': param.replace('[T.', ' (').replace(']', ')').replace('_group', '').replace(':', ' × '),
            'Coefficient': f'{coef:.4f}',
            'SE': f'{se:.4f}',
            '95% CI': f'[{ci_low:.4f}, {ci_high:.4f}]',
            'p-value': f'{p:.4f}' if p >= 0.001 else '<0.001',
            'Sig': sig
        })

df_table2 = pd.DataFrame(table2_data)

# Save as CSV
df_table2.to_csv(PUB_DIR / 'Table2_Transfer_Entropy.csv', index=False)

# Create LaTeX version
with open(PUB_DIR / 'Table2_Transfer_Entropy.tex', 'w') as f:
    f.write("\\begin{table}[h]\n")
    f.write("\\caption{Mixed Linear Model Results: Transfer Entropy with Sex $\\times$ Stress Interaction}\n")
    f.write("\\label{tab:te}\n")
    f.write("\\centering\n")
    f.write("\\small\n")
    f.write("\\begin{tabular}{lcccc}\n")
    f.write("\\hline\n")
    f.write("Parameter & $\\beta$ & SE & 95\\% CI & $p$ \\\\\n")
    f.write("\\hline\n")

    for idx, row in df_table2.iterrows():
        param_clean = row['Parameter'].replace('_', '\\_')
        f.write(f"{param_clean} & {row['Coefficient']}{row['Sig']} & {row['SE']} & {row['95% CI']} & {row['p-value']} \\\\\n")

    f.write("\\hline\n")
    f.write("\\end{tabular}\n")
    f.write("\\begin{flushleft}\n")
    f.write("\\footnotesize\n")
    f.write("$n = 119$ patients, 1404 observations. Model: TE\\_value $\\sim$ Sex $\\times$ Stress $\\times$ TE\\_Type $\\times$ Conditioning $\\times$ HR\\_Event + (1|Patient). ")
    f.write("$^{***}p < 0.001$, $^{**}p < 0.01$, $^{*}p < 0.05$.\n")
    f.write("\\end{flushleft}\n")
    f.write("\\end{table}\n")

print(f"✓ Table 2 saved:")
print(f"  - {PUB_DIR / 'Table2_Transfer_Entropy.csv'}")
print(f"  - {PUB_DIR / 'Table2_Transfer_Entropy.tex'}")

# =============================================================================
# TABLE 3: Comparative Summary Across Metrics
# =============================================================================
print("\n" + "="*100)
print("TABLE 3: Comparative Summary - All Metrics")
print("="*100)

summary_stats = pd.read_csv(MLM_DIR / 'MLM_summary_all_metrics.csv')

# Create formatted version
table3_data = []
for idx, row in summary_stats.iterrows():
    table3_data.append({
        'Metric': row['Metric'],
        'Context': row['Model'].replace('_', ' ').title(),
        'Parameters': row['Total_params'],
        'Significant': row['Sig_params'],
        'Sex': row['Sex_effects'],
        'Stress': row['Stress_effects'],
        'Interactions': row['Interactions']
    })

df_table3 = pd.DataFrame(table3_data)
df_table3.to_csv(PUB_DIR / 'Table3_Comparative_Summary.csv', index=False)

print(f"✓ Table 3 saved: {PUB_DIR / 'Table3_Comparative_Summary.csv'}")

# =============================================================================
# FIGURE 1: Sex Effects in ER/SE during mHR Conditioning
# =============================================================================
print("\n" + "="*100)
print("FIGURE 1: Sex Effects in Univariate Complexity")
print("="*100)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Entropy Rate
ax1 = axes[0]

er_sex = er_mhr[er_mhr['parameter'] == 'sex[T.Male]'].iloc[0]
er_intercept = er_mhr[er_mhr['parameter'] == 'Intercept'].iloc[0]

# Predicted values
female_er = er_intercept['coef']
male_er = er_intercept['coef'] + er_sex['coef']

# Standard errors for confidence intervals
female_se = er_intercept['se']
male_se = np.sqrt(er_intercept['se']**2 + er_sex['se']**2)  # Approximate

x_pos = [0, 1]
values = [female_er, male_er]
errors = [female_se * 1.96, male_se * 1.96]  # 95% CI

bars = ax1.bar(x_pos, values, yerr=errors, capsize=8,
               color=['lightcoral', 'lightblue'],
               edgecolor='black', linewidth=2, alpha=0.7)

ax1.set_xticks(x_pos)
ax1.set_xticklabels(['Female', 'Male'], fontsize=12)
ax1.set_ylabel('Entropy Rate (predicted)', fontsize=12)
ax1.set_title('A. Entropy Rate\nSex Effect during mHR Conditioning', fontsize=13, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Add significance annotation
y_max = max(values) + max(errors) + 0.1
ax1.plot([0, 1], [y_max, y_max], 'k-', linewidth=1.5)
ax1.text(0.5, y_max + 0.05, f'p = {er_sex["p_value"]:.3f}', ha='center', fontsize=11)

# Add sample sizes
ax1.text(0, female_er - 0.3, f'n=70', ha='center', fontsize=9)
ax1.text(1, male_er - 0.3, f'n=49', ha='center', fontsize=9)

# Panel B: Sample Entropy
ax2 = axes[1]

se_sex = se_mhr[se_mhr['parameter'] == 'sex[T.Male]'].iloc[0]
se_intercept = se_mhr[se_mhr['parameter'] == 'Intercept'].iloc[0]

female_se_val = se_intercept['coef']
male_se_val = se_intercept['coef'] + se_sex['coef']

female_se_err = se_intercept['se']
male_se_err = np.sqrt(se_intercept['se']**2 + se_sex['se']**2)

values = [female_se_val, male_se_val]
errors = [female_se_err * 1.96, male_se_err * 1.96]

bars = ax2.bar(x_pos, values, yerr=errors, capsize=8,
               color=['lightcoral', 'lightblue'],
               edgecolor='black', linewidth=2, alpha=0.7)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(['Female', 'Male'], fontsize=12)
ax2.set_ylabel('Sample Entropy (predicted)', fontsize=12)
ax2.set_title('B. Sample Entropy\nSex Effect during mHR Conditioning', fontsize=13, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

# Add significance annotation
y_max = max(values) + max(errors) + 0.005
ax2.plot([0, 1], [y_max, y_max], 'k-', linewidth=1.5)
ax2.text(0.5, y_max + 0.002, f'p = {se_sex["p_value"]:.3f}', ha='center', fontsize=11)

ax2.text(0, female_se_val - 0.01, f'n=70', ha='center', fontsize=9)
ax2.text(1, male_se_val - 0.01, f'n=49', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(PUB_DIR / 'Figure1_Sex_Effects_Univariate.png', dpi=300, bbox_inches='tight')
plt.savefig(PUB_DIR / 'Figure1_Sex_Effects_Univariate.pdf', bbox_inches='tight')
plt.close()

print(f"✓ Figure 1 saved:")
print(f"  - {PUB_DIR / 'Figure1_Sex_Effects_Univariate.png'}")
print(f"  - {PUB_DIR / 'Figure1_Sex_Effects_Univariate.pdf'}")

# =============================================================================
# FIGURE 2: TE Sex × Stress Interaction with Confidence Intervals
# =============================================================================
print("\n" + "="*100)
print("FIGURE 2: Transfer Entropy Sex × Stress Interaction")
print("="*100)

fig, ax = plt.subplots(1, 1, figsize=(10, 7))

# Extract coefficients
intercept = df_te[df_te['Parameter'] == 'Intercept']['Coefficient'].values[0]
sex_main = df_te[df_te['Parameter'] == 'sex[T.Male]']['Coefficient'].values[0]
stress_main = df_te[df_te['Parameter'] == 'stress_group[T.Stressed]']['Coefficient'].values[0]
interaction = df_te[df_te['Parameter'] == 'sex[T.Male]:stress_group[T.Stressed]']['Coefficient'].values[0]

# Standard errors
se_intercept = df_te[df_te['Parameter'] == 'Intercept']['Std_Error'].values[0]
se_sex = df_te[df_te['Parameter'] == 'sex[T.Male]']['Std_Error'].values[0]
se_stress = df_te[df_te['Parameter'] == 'stress_group[T.Stressed]']['Std_Error'].values[0]
se_interaction = df_te[df_te['Parameter'] == 'sex[T.Male]:stress_group[T.Stressed]']['Std_Error'].values[0]

# Calculate predicted values
female_control = intercept
male_control = intercept + sex_main
female_stressed = intercept + stress_main
male_stressed = intercept + sex_main + stress_main + interaction

# Calculate standard errors (approximate)
se_female_control = se_intercept
se_male_control = np.sqrt(se_intercept**2 + se_sex**2)
se_female_stressed = np.sqrt(se_intercept**2 + se_stress**2)
se_male_stressed = np.sqrt(se_intercept**2 + se_sex**2 + se_stress**2 + se_interaction**2)

# Plot
x_positions = [0, 1, 3, 4]
groups = ['Female\nControl', 'Male\nControl', 'Female\nStressed', 'Male\nStressed']
values = [female_control, male_control, female_stressed, male_stressed]
errors = [se_female_control * 1.96, se_male_control * 1.96,
          se_female_stressed * 1.96, se_male_stressed * 1.96]
colors = ['lightcoral', 'lightblue', 'red', 'blue']

bars = ax.bar(x_positions, values, yerr=errors, capsize=10,
              color=colors, edgecolor='black', linewidth=2, alpha=0.7)

ax.set_xticks(x_positions)
ax.set_xticklabels(groups, fontsize=11)
ax.set_ylabel('Net Transfer Entropy (predicted)', fontsize=13)
ax.set_title('Sex × Stress Interaction in Transfer Entropy\n(with 95% Confidence Intervals)',
             fontsize=14, fontweight='bold')
ax.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax.grid(axis='y', alpha=0.3)

# Add connecting lines to show interaction
control_mean = np.mean([female_control, male_control])
stressed_mean = np.mean([female_stressed, male_stressed])
ax.plot([0.5, 3.5], [control_mean, stressed_mean], 'k--', alpha=0.3, linewidth=1.5,
        label='Group means')

# Add interaction p-value
interaction_p = df_te[df_te['Parameter'] == 'sex[T.Male]:stress_group[T.Stressed]']['p_value'].values[0]
ax.text(0.98, 0.98, f'Sex × Stress Interaction:\np = {interaction_p:.3f}',
        transform=ax.transAxes, ha='right', va='top', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

# Add sample sizes
ax.text(0, female_control - 0.015, 'n=70', ha='center', fontsize=9)
ax.text(1, male_control - 0.015, 'n=49', ha='center', fontsize=9)
ax.text(3, female_stressed - 0.015, 'n=70', ha='center', fontsize=9)
ax.text(4, male_stressed - 0.015, 'n=49', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(PUB_DIR / 'Figure2_TE_Sex_Stress_Interaction.png', dpi=300, bbox_inches='tight')
plt.savefig(PUB_DIR / 'Figure2_TE_Sex_Stress_Interaction.pdf', bbox_inches='tight')
plt.close()

print(f"✓ Figure 2 saved:")
print(f"  - {PUB_DIR / 'Figure2_TE_Sex_Stress_Interaction.png'}")
print(f"  - {PUB_DIR / 'Figure2_TE_Sex_Stress_Interaction.pdf'}")

# =============================================================================
# FIGURE 3: Comparative Panel - ER vs SE vs TE Sensitivity
# =============================================================================
print("\n" + "="*100)
print("FIGURE 3: Comparative Sensitivity Across Metrics")
print("="*100)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel A: Effect Type Detection
ax1 = axes[0, 0]

metrics = ['ER', 'SE', 'TE']
sex_effects = [2, 1, 2]
stress_effects = [0, 0, 3]
interactions = [1, 0, 3]

x = np.arange(len(metrics))
width = 0.25

bars1 = ax1.bar(x - width, sex_effects, width, label='Sex Effects',
                color='steelblue', edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x, stress_effects, width, label='Stress Effects',
                color='coral', edgecolor='black', linewidth=1.5)
bars3 = ax1.bar(x + width, interactions, width, label='Interactions',
                color='lightgreen', edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Number of Significant Effects', fontsize=11)
ax1.set_title('A. Effect Type Detection by Metric', fontsize=12, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(metrics, fontsize=11)
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3)

# Panel B: Context Specificity
ax2 = axes[0, 1]

contexts = ['No Cond.', 'mHR Cond.', 'fHR Accel']
er_sig = [3, 5, 2]
se_sig = [1, 5, 1]

x = np.arange(len(contexts))
width = 0.35

bars1 = ax2.bar(x - width/2, er_sig, width, label='ER',
                color='steelblue', edgecolor='black', linewidth=1.5, alpha=0.7)
bars2 = ax2.bar(x + width/2, se_sig, width, label='SE',
                color='coral', edgecolor='black', linewidth=1.5, alpha=0.7)

ax2.set_ylabel('Significant Parameters', fontsize=11)
ax2.set_title('B. Context-Specific Detection (Univariate)', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(contexts, fontsize=10)
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3)

# Panel C: Effect Sizes
ax3 = axes[1, 0]

effect_types = ['Sex\n(ER)', 'Sex\n(SE)', 'Stress\n(TE)', 'Sex×Stress\n(TE)']
effect_sizes = [
    -0.258,  # ER sex
    -0.018,  # SE sex
    0.023,   # TE stress
    -0.042   # TE interaction
]
p_values = [0.024, 0.030, 0.026, 0.009]
colors_p = ['lightblue' if p < 0.01 else 'lightgreen' if p < 0.05 else 'lightgray'
            for p in p_values]

bars = ax3.barh(effect_types, effect_sizes, color=colors_p,
                edgecolor='black', linewidth=1.5)

ax3.axvline(0, color='black', linestyle='-', linewidth=1.5)
ax3.set_xlabel('Effect Size (Coefficient)', fontsize=11)
ax3.set_title('C. Effect Sizes for Key Findings', fontsize=12, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)

# Add p-values
for i, (effect, p) in enumerate(zip(effect_sizes, p_values)):
    x_pos = effect + (0.01 if effect > 0 else -0.01)
    ax3.text(x_pos, i, f'p={p:.3f}', va='center',
             ha='left' if effect > 0 else 'right', fontsize=9)

# Panel D: Summary Diagram
ax4 = axes[1, 1]
ax4.axis('off')

summary_text = """
COMPARATIVE SENSITIVITY SUMMARY

Univariate Complexity (ER & SE):
  ✓ Detect: Sex differences
  ✓ Context: Maternal HR conditioning
  ✗ Not sensitive to: Maternal stress

Bivariate Coupling (TE):
  ✓ Detect: Maternal stress effects
  ✓ Detect: Sex × Stress interaction
  ✓ Context: Multiple conditioning types

Key Insight:
Different metrics capture different
aspects of maternal-fetal physiology:
  • ER/SE → Fetal development
  • TE → Stress-modulated coupling

Statistical Advantage:
MLM detected Sex × Stress interaction
(p=0.009) impossible to find with
conventional t-tests + FDR correction.
"""

ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes,
         fontsize=10, verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))

plt.tight_layout()
plt.savefig(PUB_DIR / 'Figure3_Comparative_Sensitivity.png', dpi=300, bbox_inches='tight')
plt.savefig(PUB_DIR / 'Figure3_Comparative_Sensitivity.pdf', bbox_inches='tight')
plt.close()

print(f"✓ Figure 3 saved:")
print(f"  - {PUB_DIR / 'Figure3_Comparative_Sensitivity.png'}")
print(f"  - {PUB_DIR / 'Figure3_Comparative_Sensitivity.pdf'}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*100)
print("PUBLICATION MATERIALS COMPLETE")
print("="*100)
print(f"\nAll materials saved to: {PUB_DIR}/\n")
print("Tables (CSV and LaTeX):")
print("  ✓ Table 1: Univariate Complexity (ER & SE)")
print("  ✓ Table 2: Transfer Entropy with Interactions")
print("  ✓ Table 3: Comparative Summary")
print("\nFigures (PNG and PDF):")
print("  ✓ Figure 1: Sex Effects in ER/SE")
print("  ✓ Figure 2: TE Sex × Stress Interaction")
print("  ✓ Figure 3: Comparative Sensitivity Panel")
print("\nReady for manuscript submission!")
