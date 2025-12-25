"""
Generate Figures for Corrected Statistical Analysis
Creates visualizations to support Figures 6, 7, 11, 12 from manuscript
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Setup
OUTPUT_DIR = Path("analysis_output_corrected")
FIG_DIR = OUTPUT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

print("="*100)
print("GENERATING FIGURES FOR CORRECTED ANALYSIS")
print("="*100)

# Load data
df_patient = pd.read_csv(OUTPUT_DIR / "patient_level_data_corrected.csv")
df_exposure = pd.read_csv(OUTPUT_DIR / "exposure_effects_corrected.csv")
df_sex = pd.read_csv(OUTPUT_DIR / "sex_effects_corrected.csv")

print(f"\nLoaded data:")
print(f"  Patient-level: {len(df_patient)} patients")
print(f"  Exposure results: {len(df_exposure)} features")
print(f"  Sex results: {len(df_sex)} features")

# Figure 1: Forest Plot - Exposure Effects
print("\nGenerating Figure 1: Forest Plot - Exposure Effects...")
fig, ax = plt.subplots(figsize=(10, 12))

# Sort by effect size
df_exp_sorted = df_exposure.sort_values('cohens_d')

y_pos = np.arange(len(df_exp_sorted))
ax.errorbar(df_exp_sorted['cohens_d'], y_pos,
            xerr=df_exp_sorted['cohens_d'].abs() * 0.1,  # Approximate CI
            fmt='o', markersize=6, capsize=4, alpha=0.7)

# Add reference lines
ax.axvline(0, color='black', linestyle='-', linewidth=1)
ax.axvline(-0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axvline(0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axvline(-0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
ax.axvline(0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(df_exp_sorted['feature'], fontsize=8)
ax.set_xlabel("Cohen's d (Stressed - Control)", fontsize=12)
ax.set_title("Stress Exposure Effects: Forest Plot\n(n=60 Control, n=59 Stressed)", fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / "forest_plot_exposure.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {FIG_DIR / 'forest_plot_exposure.png'}")

# Figure 2: Forest Plot - Sex Effects
print("\nGenerating Figure 2: Forest Plot - Sex Effects...")
fig, ax = plt.subplots(figsize=(10, 12))

# Sort by effect size
df_sex_sorted = df_sex.sort_values('cohens_d')

y_pos = np.arange(len(df_sex_sorted))

# Color code by significance
colors = ['red' if p < 0.05 else 'blue' for p in df_sex_sorted['pval']]

ax.errorbar(df_sex_sorted['cohens_d'], y_pos,
            xerr=df_sex_sorted['cohens_d'].abs() * 0.1,
            fmt='o', markersize=6, capsize=4, alpha=0.7)

# Highlight significant points
sig_mask = df_sex_sorted['pval'] < 0.05
if sig_mask.sum() > 0:
    ax.scatter(df_sex_sorted.loc[sig_mask, 'cohens_d'],
              y_pos[sig_mask.values],
              s=150, facecolors='none', edgecolors='red', linewidths=2,
              label='p < 0.05 (uncorrected)', zorder=10)

# Add reference lines
ax.axvline(0, color='black', linestyle='-', linewidth=1)
ax.axvline(-0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axvline(0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax.axvline(-0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)
ax.axvline(0.5, color='gray', linestyle=':', linewidth=0.5, alpha=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(df_sex_sorted['feature'], fontsize=8)
ax.set_xlabel("Cohen's d (Male - Female)", fontsize=12)
ax.set_title("Fetal Sex Effects: Forest Plot\n(n=49 Male, n=70 Female)", fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
if sig_mask.sum() > 0:
    ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig(FIG_DIR / "forest_plot_sex.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {FIG_DIR / 'forest_plot_sex.png'}")

# Figure 3: Volcano Plots
print("\nGenerating Figure 3: Volcano Plots...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Exposure volcano plot
ax1.scatter(df_exposure['cohens_d'], -np.log10(df_exposure['pval']),
           alpha=0.6, s=50)
ax1.axhline(-np.log10(0.05), color='red', linestyle='--', linewidth=1, alpha=0.7, label='p = 0.05')
ax1.axvline(-0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax1.axvline(0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax1.set_xlabel("Cohen's d (Stressed - Control)", fontsize=12)
ax1.set_ylabel("-log10(p-value)", fontsize=12)
ax1.set_title("Stress Exposure Effects", fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Sex volcano plot
colors_sex = ['red' if p < 0.05 else 'blue' for p in df_sex['pval']]
ax2.scatter(df_sex['cohens_d'], -np.log10(df_sex['pval']),
           c=colors_sex, alpha=0.6, s=50)
ax2.axhline(-np.log10(0.05), color='red', linestyle='--', linewidth=1, alpha=0.7, label='p = 0.05')
ax2.axvline(-0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax2.axvline(0.2, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
ax2.set_xlabel("Cohen's d (Male - Female)", fontsize=12)
ax2.set_ylabel("-log10(p-value)", fontsize=12)
ax2.set_title("Fetal Sex Effects", fontsize=13, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

# Add labels for significant points
sig_sex = df_sex[df_sex['pval'] < 0.05]
for _, row in sig_sex.iterrows():
    ax2.annotate(row['feature'].replace('_', ' '),
                xy=(row['cohens_d'], -np.log10(row['pval'])),
                xytext=(5, 5), textcoords='offset points',
                fontsize=8, alpha=0.7)

plt.tight_layout()
plt.savefig(FIG_DIR / "volcano_plots.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {FIG_DIR / 'volcano_plots.png'}")

# Figure 4: Violin Plots for Significant Sex Effects
if (df_sex['pval'] < 0.05).sum() > 0:
    print("\nGenerating Figure 4: Violin Plots - Significant Sex Effects...")

    sig_features = df_sex[df_sex['pval'] < 0.05]['feature'].tolist()
    n_features = len(sig_features)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, feature in enumerate(sig_features[:4]):  # Top 4
        ax = axes[idx]

        # Prepare data
        data_male = df_patient[df_patient['group_sex'] == 1][feature].dropna()
        data_female = df_patient[df_patient['group_sex'] == 0][feature].dropna()

        # Create violin plot
        parts = ax.violinplot([data_male, data_female],
                              positions=[1, 2],
                              showmeans=True, showmedians=True)

        # Add individual points
        ax.scatter(np.ones(len(data_male)) + np.random.normal(0, 0.04, len(data_male)),
                  data_male, alpha=0.3, s=20, color='blue')
        ax.scatter(np.ones(len(data_female))*2 + np.random.normal(0, 0.04, len(data_female)),
                  data_female, alpha=0.3, s=20, color='red')

        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Male\n(n={})'.format(len(data_male)),
                           'Female\n(n={})'.format(len(data_female))])
        ax.set_ylabel(feature.replace('_', ' '), fontsize=10)

        # Get stats
        result = df_sex[df_sex['feature'] == feature].iloc[0]
        ax.set_title(f"p = {result['pval']:.4f}, d = {result['cohens_d']:.3f}",
                    fontsize=11)
        ax.grid(axis='y', alpha=0.3)

    # Hide unused subplots
    for idx in range(n_features, 4):
        axes[idx].axis('off')

    fig.suptitle("Significant Sex Effects in Fetal Entropy Rate Features",
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "violin_plots_sex_effects.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIG_DIR / 'violin_plots_sex_effects.png'}")

# Figure 5: Effect Size Distributions
print("\nGenerating Figure 5: Effect Size Distributions...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Exposure effect sizes
ax1.hist(df_exposure['cohens_d'], bins=20, alpha=0.7, edgecolor='black')
ax1.axvline(0, color='red', linestyle='--', linewidth=2, label='No effect')
ax1.axvline(df_exposure['cohens_d'].mean(), color='blue', linestyle='-',
           linewidth=2, label=f'Mean = {df_exposure["cohens_d"].mean():.3f}')
ax1.set_xlabel("Cohen's d", fontsize=12)
ax1.set_ylabel("Count", fontsize=12)
ax1.set_title("Exposure Effects Distribution\n(Stressed - Control)", fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Sex effect sizes
ax2.hist(df_sex['cohens_d'], bins=20, alpha=0.7, edgecolor='black', color='orange')
ax2.axvline(0, color='red', linestyle='--', linewidth=2, label='No effect')
ax2.axvline(df_sex['cohens_d'].mean(), color='blue', linestyle='-',
           linewidth=2, label=f'Mean = {df_sex["cohens_d"].mean():.3f}')
ax2.set_xlabel("Cohen's d", fontsize=12)
ax2.set_ylabel("Count", fontsize=12)
ax2.set_title("Sex Effects Distribution\n(Male - Female)", fontsize=13, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / "effect_size_distributions.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {FIG_DIR / 'effect_size_distributions.png'}")

# Figure 6: P-value Distributions
print("\nGenerating Figure 6: P-value Distributions...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Exposure p-values
ax1.hist(df_exposure['pval'], bins=20, alpha=0.7, edgecolor='black')
ax1.axvline(0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')
ax1.set_xlabel("P-value", fontsize=12)
ax1.set_ylabel("Count", fontsize=12)
ax1.set_title("Exposure Effects P-values", fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(alpha=0.3)

# Sex p-values
ax2.hist(df_sex['pval'], bins=20, alpha=0.7, edgecolor='black', color='orange')
ax2.axvline(0.05, color='red', linestyle='--', linewidth=2, label='α = 0.05')
ax2.set_xlabel("P-value", fontsize=12)
ax2.set_ylabel("Count", fontsize=12)
ax2.set_title("Sex Effects P-values", fontsize=13, fontweight='bold')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(FIG_DIR / "pvalue_distributions.png", dpi=300, bbox_inches='tight')
plt.close()
print(f"  ✓ Saved: {FIG_DIR / 'pvalue_distributions.png'}")

print("\n" + "="*100)
print("FIGURE GENERATION COMPLETE")
print("="*100)
print(f"\nAll figures saved to: {FIG_DIR}/")
print("\nGenerated figures:")
print("  1. forest_plot_exposure.png - Forest plot of exposure effects")
print("  2. forest_plot_sex.png - Forest plot of sex effects")
print("  3. volcano_plots.png - Volcano plots for both comparisons")
print("  4. violin_plots_sex_effects.png - Distribution plots for significant sex effects")
print("  5. effect_size_distributions.png - Histogram of Cohen's d values")
print("  6. pvalue_distributions.png - Histogram of p-values")
