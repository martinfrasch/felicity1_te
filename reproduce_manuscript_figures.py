"""
Reproduce Manuscript Figures 6, 7, 11, 12
Box plots showing entropy rate and transfer entropy effects

IMPORTANT NOTES FROM DATA ANALYSIS:
- CLAUDE.md line 35: "All estimates are AUC in the [0.5-2.5]s time interval."
- entropy_rate.txt contains hAUC (mean) values ONLY, NOT hmax values
- Therefore, we can only reproduce the "mean entropy rate" portions of Figures 6 & 7
- For TE (Figures 11 & 12), we have both max and mean from separate CSV files

P-VALUE CLARIFICATION:
- P-values shown test whether mean net TE differs from 0
- H0: mean net TE = 0 (no directional information flow)
- One-sample t-test against 0
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# Setup
OUTPUT_DIR = Path("analysis_output_corrected")
FIG_DIR = OUTPUT_DIR / "manuscript_figures"
FIG_DIR.mkdir(exist_ok=True)

print("="*100)
print("REPRODUCING MANUSCRIPT FIGURES 6, 7, 11, 12")
print("="*100)
print("\n⚠️  DATA LIMITATION:")
print("entropy_rate.txt contains hAUC (mean) values only, NOT hmax (maximal) values")
print("Therefore: Figures 6 & 7 will show mean ER only (hmax not available)")
print("="*100)

# Load patient-level data with corrected groups
df = pd.read_csv(OUTPUT_DIR / "patient_level_data_corrected.csv")

print(f"\n✓ Loaded {len(df)} patients with corrected group assignments")
print(f"  Control: n={(df['group_stress'] == 0).sum()}")
print(f"  Stressed: n={(df['group_stress'] == 1).sum()}")
print(f"  Female: n={(df['group_sex'] == 0).sum()}")
print(f"  Male: n={(df['group_sex'] == 1).sum()}")

# Set plotting style
plt.style.use('default')
sns.set_palette("Set2")

# Colors
color_mother = '#4472C4'
color_fetus = '#E06666'

# Define groups for all figures
groups = [
    ('all', df, 'all'),
    ('stressed', df[df['group_stress'] == 1], 'stressed'),
    ('control', df[df['group_stress'] == 0], 'control'),
    ('male', df[df['group_sex'] == 1], 'male fetus'),
    ('female', df[df['group_sex'] == 0], 'female fetus')
]

# =============================================================================
# FIGURE 6: Entropy Rate - No Conditioning (MEAN ONLY)
# =============================================================================
print("\n" + "="*100)
print("FIGURE 6: Entropy Rate (hAUC/mean only) - No Conditioning")
print("="*100)

fig, axes = plt.subplots(1, 5, figsize=(20, 5))

# Features for Figure 6 (no conditioning) - these are hAUC values from entropy_rate.txt
features_mother_mean = 'mother_full'
features_fetus_mean = 'fetus_full'

# Single row: hAUC (mean) - hmax not available
for col_idx, (group_name, group_df, label) in enumerate(groups):
    ax = axes[col_idx]
    data_mother_mean = group_df[features_mother_mean].dropna()
    data_fetus_mean = group_df[features_fetus_mean].dropna()

    positions = [1, 2]
    bp = ax.boxplot([data_mother_mean, data_fetus_mean],
                     positions=positions,
                     widths=0.6,
                     patch_artist=True,
                     showfliers=True,
                     boxprops=dict(linewidth=1.5),
                     whiskerprops=dict(linewidth=1.5),
                     capprops=dict(linewidth=1.5),
                     medianprops=dict(linewidth=2, color='black'))

    # Color boxes
    bp['boxes'][0].set_facecolor(color_mother)
    bp['boxes'][0].set_alpha(0.7)
    bp['boxes'][1].set_facecolor(color_fetus)
    bp['boxes'][1].set_alpha(0.7)

    ax.set_xticks([1, 2])
    ax.set_xticklabels(['mHR', 'fHR'], fontsize=10)
    ax.set_ylabel('mean entropy rate (hAUC)' if col_idx == 0 else '', fontsize=11)
    ax.set_title(label, fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim([1.5, 3.0])

fig.suptitle('Figure 6: Entropy Rate - No Conditioning (Mean values only)\n⚠️ hmax not available - only hAUC shown',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / 'Figure_6_ER_no_conditioning_MEAN_ONLY.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {FIG_DIR / 'Figure_6_ER_no_conditioning_MEAN_ONLY.png'}")
print(f"  ⚠️  Only mean (hAUC) values shown - hmax not available in txt files")

# =============================================================================
# FIGURE 7: Entropy Rate - With Conditioning (MEAN ONLY)
# Breakdown by sex and group
# =============================================================================
print("\n" + "="*100)
print("FIGURE 7: Entropy Rate (hAUC/mean only) - With Conditioning")
print("Breakdown by sex and group")
print("="*100)

# Conditioning types for Figure 7 - these are hAUC values
conditioning_sets = [
    ('fHR accel', 'fetus_fHR_accel', 'mother_fHR_accel'),
    ('fHR decel', 'fetus_fHR_decel', 'mother_fHR_decel'),
    ('mHR accel', 'fetus_mHR_accel', 'mother_mHR_accel'),
    ('mHR decel', 'fetus_mHR_decel', 'mother_mHR_decel')
]

fig, axes = plt.subplots(4, 5, figsize=(20, 16))

for row_idx, (cond_label, feature_fetus, feature_mother) in enumerate(conditioning_sets):
    for col_idx, (group_name, group_df, group_label) in enumerate(groups):
        ax = axes[row_idx, col_idx]

        # Check if features exist
        if feature_fetus not in df.columns or feature_mother not in df.columns:
            ax.text(0.5, 0.5, 'Data not\navailable',
                    ha='center', va='center', transform=ax.transAxes, fontsize=9)
            if row_idx == 0:
                ax.set_title(group_label, fontsize=11)
            if col_idx == 0:
                ax.set_ylabel(cond_label, fontsize=10)
            continue

        data_fetus_mean = group_df[feature_fetus].dropna()
        data_mother_mean = group_df[feature_mother].dropna()

        # Skip if no data
        if len(data_fetus_mean) == 0 and len(data_mother_mean) == 0:
            ax.text(0.5, 0.5, f'n=0',
                    ha='center', va='center', transform=ax.transAxes, fontsize=9)
            if row_idx == 0:
                ax.set_title(group_label, fontsize=11)
            if col_idx == 0:
                ax.set_ylabel(cond_label, fontsize=10)
            continue

        bp = ax.boxplot([data_mother_mean, data_fetus_mean],
                         positions=[1, 2],
                         widths=0.5,
                         patch_artist=True,
                         showfliers=True,
                         boxprops=dict(linewidth=1.2),
                         whiskerprops=dict(linewidth=1.2),
                         capprops=dict(linewidth=1.2),
                         medianprops=dict(linewidth=1.5, color='black'))

        bp['boxes'][0].set_facecolor(color_mother)
        bp['boxes'][0].set_alpha(0.7)
        bp['boxes'][1].set_facecolor(color_fetus)
        bp['boxes'][1].set_alpha(0.7)

        ax.set_xticks([1, 2])
        ax.set_xticklabels(['mHR', 'fHR'], fontsize=8)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim([0.8, 3.2])

        # Add title only to top row
        if row_idx == 0:
            ax.set_title(group_label, fontsize=11)

        # Add ylabel only to leftmost column
        if col_idx == 0:
            ax.set_ylabel(f'{cond_label}\nmean ER (hAUC)', fontsize=9)

fig.suptitle('Figure 7: Entropy Rate - With Conditioning (Mean values only, breakdown by sex/group)\n⚠️ hmax not available - only hAUC shown',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / 'Figure_7_ER_with_conditioning_MEAN_ONLY.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {FIG_DIR / 'Figure_7_ER_with_conditioning_MEAN_ONLY.png'}")
print(f"  ⚠️  Only mean (hAUC) values shown - hmax not available in txt files")

# =============================================================================
# FIGURE 11: Transfer Entropy - No Conditioning
# Breakdown by sex and group
# =============================================================================
print("\n" + "="*100)
print("FIGURE 11: Transfer Entropy - No Conditioning (Both max and mean)")
print("Breakdown by sex and group")
print("="*100)

fig, axes = plt.subplots(2, 5, figsize=(20, 8))

# Row 0: TEmax
# Row 1: TEmean
te_features = [
    ('max_TE_mHR_all', 'max value TE$_{max}$', 'lightblue'),
    ('mean_TE_mHR_all', 'mean value TE$_{AUC}$', 'lightgreen')
]

for row_idx, (feature, row_label, box_color) in enumerate(te_features):
    for col_idx, (group_name, group_df, group_label) in enumerate(groups):
        ax = axes[row_idx, col_idx]

        te_data = group_df[feature].dropna()

        if len(te_data) == 0:
            ax.text(0.5, 0.5, f'n=0',
                    ha='center', va='center', transform=ax.transAxes)
            if row_idx == 0:
                ax.set_title(group_label, fontsize=11)
            if col_idx == 0:
                ax.set_ylabel(row_label, fontsize=10)
            continue

        bp = ax.boxplot([te_data],
                         positions=[1],
                         widths=0.5,
                         patch_artist=True,
                         showfliers=True,
                         boxprops=dict(linewidth=1.5, facecolor=box_color, alpha=0.7),
                         whiskerprops=dict(linewidth=1.5),
                         capprops=dict(linewidth=1.5),
                         medianprops=dict(linewidth=2, color='black'))

        ax.set_xticks([1])
        ax.set_xticklabels(['net'], fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        ax.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
        ax.set_ylim([-0.05, 0.15])

        # Compute p-value (one-sample t-test against 0)
        t_stat, p_val = stats.ttest_1samp(te_data, 0)
        ax.text(0.98, 0.98, f'p={p_val:.3f}\nn={len(te_data)}',
               transform=ax.transAxes,
               ha='right', va='top', fontsize=8,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Add title only to top row
        if row_idx == 0:
            ax.set_title(group_label, fontsize=11)

        # Add ylabel only to leftmost column
        if col_idx == 0:
            ax.set_ylabel(row_label, fontsize=10)

fig.suptitle('Figure 11: Transfer Entropy - No Conditioning (breakdown by sex/group)\nP-values: one-sample t-test H₀: mean net TE = 0',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / 'Figure_11_TE_no_conditioning.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {FIG_DIR / 'Figure_11_TE_no_conditioning.png'}")
print(f"  P-values test H₀: mean net TE = 0 (one-sample t-test)")

# =============================================================================
# FIGURE 12: Transfer Entropy - With Conditioning
# Breakdown by sex and group
# =============================================================================
print("\n" + "="*100)
print("FIGURE 12: Transfer Entropy - With Conditioning (Both max and mean)")
print("Breakdown by sex and group")
print("="*100)

# Conditioning sets for Figure 12
te_conditions = [
    ('mHR accel', 'max_TE_mHR_accel', 'mean_TE_mHR_accel'),
    ('mHR decel', 'max_TE_mHR_decel', 'mean_TE_mHR_decel'),
    ('fHR accel', 'max_TE_fHR_accel', 'mean_TE_fHR_accel'),
    ('fHR decel', 'max_TE_fHR_decel', 'mean_TE_fHR_decel')
]

fig, axes = plt.subplots(2, 4, figsize=(18, 10))

for col_idx, (cond_label, feature_max, feature_mean) in enumerate(te_conditions):

    # TEmax (top row) - show all 5 groups as separate boxes
    ax_top = axes[0, col_idx]

    data_list_max = []
    labels_max = []
    colors_max = []
    group_colors = ['gray', 'red', 'blue', 'green', 'orange']

    for g_idx, (group_name, group_df, group_label) in enumerate(groups):
        te_data = group_df[feature_max].dropna()
        if len(te_data) > 0:
            data_list_max.append(te_data)
            labels_max.append(f'{group_label}\n(n={len(te_data)})')
            colors_max.append(group_colors[g_idx])

    if len(data_list_max) > 0:
        bp = ax_top.boxplot(data_list_max,
                             positions=range(1, len(data_list_max) + 1),
                             widths=0.6,
                             patch_artist=True,
                             showfliers=True,
                             boxprops=dict(linewidth=1.2),
                             whiskerprops=dict(linewidth=1.2),
                             capprops=dict(linewidth=1.2),
                             medianprops=dict(linewidth=1.5, color='black'))

        # Color boxes
        for patch, color in zip(bp['boxes'], colors_max):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        ax_top.set_xticks(range(1, len(labels_max) + 1))
        ax_top.set_xticklabels(labels_max, fontsize=7)
        ax_top.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
        ax_top.set_ylim([-0.05, 0.15])

        # Compute p-value for 'all' group (first one)
        if len(data_list_max) > 0:
            t_stat, p_val = stats.ttest_1samp(data_list_max[0], 0)
            ax_top.text(0.02, 0.98, f'p(all)={p_val:.3f}',
                       transform=ax_top.transAxes,
                       ha='left', va='top', fontsize=8,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax_top.set_ylabel('max TE$_{max}$' if col_idx == 0 else '', fontsize=10)
    ax_top.set_title(f'{cond_label}', fontsize=11)
    ax_top.grid(axis='y', alpha=0.3)

    # TEauc/mean (bottom row) - show all 5 groups as separate boxes
    ax_bottom = axes[1, col_idx]

    data_list_mean = []
    labels_mean = []
    colors_mean = []

    for g_idx, (group_name, group_df, group_label) in enumerate(groups):
        te_data = group_df[feature_mean].dropna()
        if len(te_data) > 0:
            data_list_mean.append(te_data)
            labels_mean.append(f'{group_label}\n(n={len(te_data)})')
            colors_mean.append(group_colors[g_idx])

    if len(data_list_mean) > 0:
        bp = ax_bottom.boxplot(data_list_mean,
                                positions=range(1, len(data_list_mean) + 1),
                                widths=0.6,
                                patch_artist=True,
                                showfliers=True,
                                boxprops=dict(linewidth=1.2),
                                whiskerprops=dict(linewidth=1.2),
                                capprops=dict(linewidth=1.2),
                                medianprops=dict(linewidth=1.5, color='black'))

        # Color boxes
        for patch, color in zip(bp['boxes'], colors_mean):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)

        ax_bottom.set_xticks(range(1, len(labels_mean) + 1))
        ax_bottom.set_xticklabels(labels_mean, fontsize=7)
        ax_bottom.axhline(0, color='red', linestyle='--', linewidth=1, alpha=0.5)
        ax_bottom.set_ylim([-0.04, 0.06])

        # Compute p-value for 'all' group (first one)
        if len(data_list_mean) > 0:
            t_stat, p_val = stats.ttest_1samp(data_list_mean[0], 0)
            ax_bottom.text(0.02, 0.98, f'p(all)={p_val:.3f}',
                          transform=ax_bottom.transAxes,
                          ha='left', va='top', fontsize=8,
                          bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax_bottom.set_ylabel('mean TE$_{AUC}$' if col_idx == 0 else '', fontsize=10)
    ax_bottom.grid(axis='y', alpha=0.3)

fig.suptitle('Figure 12: Transfer Entropy - With Conditioning (breakdown by sex/group)\nP-values: one-sample t-test H₀: mean net TE = 0 (for "all" group only)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(FIG_DIR / 'Figure_12_TE_with_conditioning.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✓ Saved: {FIG_DIR / 'Figure_12_TE_with_conditioning.png'}")
print(f"  P-values test H₀: mean net TE = 0 (one-sample t-test, 'all' group only)")

# =============================================================================
# Summary Report
# =============================================================================
print("\n" + "="*100)
print("MANUSCRIPT FIGURES REPRODUCED (with data limitations noted)")
print("="*100)
print(f"\nAll figures saved to: {FIG_DIR}/\n")
print("Generated:")
print("  ✓ Figure 6: Entropy rate - no conditioning (MEAN ONLY)")
print("  ✓ Figure 7: Entropy rate - with conditioning (MEAN ONLY) + SEX/GROUP BREAKDOWN")
print("  ✓ Figure 11: Transfer entropy - no conditioning (BOTH max and mean) + SEX/GROUP BREAKDOWN")
print("  ✓ Figure 12: Transfer entropy - with conditioning (BOTH max and mean) + SEX/GROUP BREAKDOWN")
print("\nData Limitations:")
print("  ⚠️  Entropy rate: Only hAUC (mean) available from txt files, NOT hmax")
print("  ✓  Transfer entropy: Both max and mean available from CSV files")
print("\nP-value Interpretation:")
print("  - P-values shown are from one-sample t-test against 0")
print("  - H₀: mean net TE = 0 (no directional information flow)")
print("  - Tests whether maternal→fetal information flow differs significantly from zero")
print("\nNote: Groups have been corrected based on groups_scores_new.xlsx as ground truth")
print(f"      Control: n=60, Stressed: n=59, Male: n=49, Female: n=70")
