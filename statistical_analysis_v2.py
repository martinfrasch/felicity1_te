#!/usr/bin/env python3
"""
Statistical Analysis for Figures 3, 4, 6, and 7 (NaN-aware version)
- Figures 3 & 4: Acceleration/deceleration ratios
- Figures 6 & 7: Hmax/Hmean entropy rate values
"""

import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PART 1: Acceleration/Deceleration Counts Analysis (Figures 3 & 4)
# ============================================================================

def load_accel_decel_data():
    """Load and organize accel/decel count data"""

    mhr_file = np.load('accel_decel_counts_values/accel_deccel_maternalHR_conditioning.npz')
    fhr_file = np.load('accel_decel_counts_values/accel_deccel_fetalHR_conditioning.npz')

    print("=== ACCEL/DECEL COUNTS DATA STRUCTURE ===\n")
    print("Maternal HR conditioning arrays:", mhr_file.files)
    print("Fetal HR conditioning arrays:", fhr_file.files)
    print()

    return mhr_file, fhr_file

def compute_ratios_and_stats(data_file, conditioning_type):
    """Compute fractions and ratios from count data"""

    results = {}

    groups = ['', '_stressed', '_control', '_male', '_female']
    group_names = ['all', 'stressed', 'control', 'male', 'female']

    for group, name in zip(groups, group_names):
        N_total = data_file[f'N_total{group}']
        N_accel = data_file[f'N_accel{group}']
        N_decel = data_file[f'N_decel{group}']

        frac_accel = N_accel / N_total
        frac_decel = N_decel / N_total
        ratio_decel_accel = N_decel / N_accel

        results[name] = {
            'N_total': N_total,
            'N_accel': N_accel,
            'N_decel': N_decel,
            'frac_accel': frac_accel,
            'frac_decel': frac_decel,
            'ratio_decel_accel': ratio_decel_accel
        }

    return results

def statistical_tests_accel_decel(mhr_results, fhr_results):
    """Perform statistical tests for Figure 3 and 4"""

    print("\n" + "="*80)
    print("STATISTICAL TESTS: ACCEL/DECEL RATIOS (Figures 3 & 4)")
    print("="*80 + "\n")

    # ========================================================================
    # Figure 3 Tests: Overall statistics
    # ========================================================================
    print("="*80)
    print("FIGURE 3: OVERALL ACCEL/DECEL STATISTICS")
    print("="*80 + "\n")

    for cond_name, results in [('Maternal HR', mhr_results), ('Fetal HR', fhr_results)]:
        print(f"\n--- {cond_name} Conditioning ---\n")

        all_data = results['all']

        print("Test: Fraction of accelerations vs 0.5 (null: no preference)")
        t_stat, p_val = stats.ttest_1samp(all_data['frac_accel'], 0.5)
        print(f"  Mean frac_accel: {np.mean(all_data['frac_accel']):.4f} ± {np.std(all_data['frac_accel']):.4f}")
        print(f"  t = {t_stat:.4f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        print("\nTest: Fraction of decelerations vs 0.5")
        t_stat, p_val = stats.ttest_1samp(all_data['frac_decel'], 0.5)
        print(f"  Mean frac_decel: {np.mean(all_data['frac_decel']):.4f} ± {np.std(all_data['frac_decel']):.4f}")
        print(f"  t = {t_stat:.4f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        print("\nTest: Decel/Accel ratio vs 1.0 (null: equal occurrence)")
        t_stat, p_val = stats.ttest_1samp(all_data['ratio_decel_accel'], 1.0)
        print(f"  Mean ratio: {np.mean(all_data['ratio_decel_accel']):.4f} ± {np.std(all_data['ratio_decel_accel']):.4f}")
        print(f"  t = {t_stat:.4f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

    # ========================================================================
    # Figure 4 Tests: Group comparisons
    # ========================================================================
    print("\n\n" + "="*80)
    print("FIGURE 4: GROUP COMPARISONS")
    print("="*80 + "\n")

    for cond_name, results in [('Maternal HR', mhr_results), ('Fetal HR', fhr_results)]:
        print(f"\n{'='*60}")
        print(f"{cond_name} Conditioning")
        print('='*60 + "\n")

        stressed = results['stressed']
        control = results['control']

        print("--- STRESS GROUP COMPARISON ---\n")

        print("Fraction of accelerations:")
        u_stat, p_val = stats.mannwhitneyu(stressed['frac_accel'], control['frac_accel'], alternative='two-sided')
        print(f"  Stressed: {np.mean(stressed['frac_accel']):.4f} ± {np.std(stressed['frac_accel']):.4f} (n={len(stressed['frac_accel'])})")
        print(f"  Control:  {np.mean(control['frac_accel']):.4f} ± {np.std(control['frac_accel']):.4f} (n={len(control['frac_accel'])})")
        print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        print("\nFraction of decelerations:")
        u_stat, p_val = stats.mannwhitneyu(stressed['frac_decel'], control['frac_decel'], alternative='two-sided')
        print(f"  Stressed: {np.mean(stressed['frac_decel']):.4f} ± {np.std(stressed['frac_decel']):.4f}")
        print(f"  Control:  {np.mean(control['frac_decel']):.4f} ± {np.std(control['frac_decel']):.4f}")
        print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        print("\nDecel/Accel ratio:")
        u_stat, p_val = stats.mannwhitneyu(stressed['ratio_decel_accel'], control['ratio_decel_accel'], alternative='two-sided')
        print(f"  Stressed: {np.mean(stressed['ratio_decel_accel']):.4f} ± {np.std(stressed['ratio_decel_accel']):.4f}")
        print(f"  Control:  {np.mean(control['ratio_decel_accel']):.4f} ± {np.std(control['ratio_decel_accel']):.4f}")
        print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        male = results['male']
        female = results['female']

        print("\n--- SEX GROUP COMPARISON ---\n")

        print("Fraction of accelerations:")
        u_stat, p_val = stats.mannwhitneyu(male['frac_accel'], female['frac_accel'], alternative='two-sided')
        print(f"  Male:   {np.mean(male['frac_accel']):.4f} ± {np.std(male['frac_accel']):.4f} (n={len(male['frac_accel'])})")
        print(f"  Female: {np.mean(female['frac_accel']):.4f} ± {np.std(female['frac_accel']):.4f} (n={len(female['frac_accel'])})")
        print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        print("\nFraction of decelerations:")
        u_stat, p_val = stats.mannwhitneyu(male['frac_decel'], female['frac_decel'], alternative='two-sided')
        print(f"  Male:   {np.mean(male['frac_decel']):.4f} ± {np.std(male['frac_decel']):.4f}")
        print(f"  Female: {np.mean(female['frac_decel']):.4f} ± {np.std(female['frac_decel']):.4f}")
        print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

        print("\nDecel/Accel ratio:")
        u_stat, p_val = stats.mannwhitneyu(male['ratio_decel_accel'], female['ratio_decel_accel'], alternative='two-sided')
        print(f"  Male:   {np.mean(male['ratio_decel_accel']):.4f} ± {np.std(male['ratio_decel_accel']):.4f}")
        print(f"  Female: {np.mean(female['ratio_decel_accel']):.4f} ± {np.std(female['ratio_decel_accel']):.4f}")
        print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")


# ============================================================================
# PART 2: Hmax/Hmean Values Analysis (Figures 6 & 7) - NaN-aware
# ============================================================================

def load_hmax_data():
    """Load all hmax and hmean data files"""

    print("\n\n" + "="*80)
    print("HMAX/HMEAN DATA LOADING (Figures 6 & 7)")
    print("="*80 + "\n")

    hmax_dir = Path('hmax_values')

    hmax_files = sorted(hmax_dir.glob('hmax_*.npz'))
    hmean_files = sorted(hmax_dir.glob('hmean_*.npz'))

    print(f"Found {len(hmax_files)} hmax files and {len(hmean_files)} hmean files\n")

    hmax_data = {}
    hmean_data = {}

    for file in hmax_files:
        data = np.load(file)
        key = file.stem.replace('hmax_', '')
        hmax_data[key] = {
            'all': data['all'],
            'stressed': data['stressed'],
            'control': data['control'],
            'male': data['male'],
            'female': data['female']
        }

    for file in hmean_files:
        data = np.load(file)
        key = file.stem.replace('hmean_', '')
        hmean_data[key] = {
            'all': data['all'],
            'stressed': data['stressed'],
            'control': data['control'],
            'male': data['male'],
            'female': data['female']
        }

    print(f"Loaded conditions: {list(hmax_data.keys())}")

    return hmax_data, hmean_data

def statistical_tests_hmax(hmax_data, hmean_data):
    """Perform statistical tests on hmax/hmean data (NaN-aware)"""

    print("\n\n" + "="*80)
    print("STATISTICAL TESTS: ENTROPY RATE (HMAX/HMEAN) - Figures 6 & 7")
    print("="*80 + "\n")

    conditions_to_test = [
        'fetus_no_conditoning',
        'mother_no_conditoning',
        'fetus_mother_accel',
        'fetus_mother_decel',
        'mother_fetus_accel',
        'mother_fetus_decel',
        'fetus_fetus_accel',
        'fetus_fetus_decel',
        'mother_mother_accel',
        'mother_mother_decel'
    ]

    for metric_name, data_dict in [('HMAX', hmax_data), ('HMEAN', hmean_data)]:
        print(f"\n{'='*80}")
        print(f"{metric_name} ANALYSIS")
        print('='*80)

        for condition in conditions_to_test:
            if condition not in data_dict:
                continue

            print(f"\n--- {condition.replace('_', ' ').title()} ---\n")

            data = data_dict[condition]

            # Filter out NaN values
            stressed = data['stressed'][~np.isnan(data['stressed'])]
            control = data['control'][~np.isnan(data['control'])]
            male = data['male'][~np.isnan(data['male'])]
            female = data['female'][~np.isnan(data['female'])]

            # Skip if no valid data
            if len(stressed) == 0 or len(control) == 0:
                print("Stressed vs Control: Insufficient data (all NaN)")
            else:
                print("Stressed vs Control:")
                u_stat, p_val = stats.mannwhitneyu(stressed, control, alternative='two-sided')
                print(f"  Stressed: {np.mean(stressed):.4f} ± {np.std(stressed):.4f} (n={len(stressed)})")
                print(f"  Control:  {np.mean(control):.4f} ± {np.std(control):.4f} (n={len(control)})")
                print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")

            if len(male) == 0 or len(female) == 0:
                print("\nMale vs Female: Insufficient data (all NaN)")
            else:
                print("\nMale vs Female:")
                u_stat, p_val = stats.mannwhitneyu(male, female, alternative='two-sided')
                print(f"  Male:   {np.mean(male):.4f} ± {np.std(male):.4f} (n={len(male)})")
                print(f"  Female: {np.mean(female):.4f} ± {np.std(female):.4f} (n={len(female)})")
                print(f"  Mann-Whitney U = {u_stat:.1f}, p = {p_val:.6f} {'***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else 'ns'}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "="*80)
    print("COMPREHENSIVE STATISTICAL ANALYSIS (NaN-aware)")
    print("Figures 3 & 4: Accel/Decel Ratios")
    print("Figures 6 & 7: Hmax/Hmean Entropy Rate Values")
    print("="*80)

    # Part 1: Accel/Decel Analysis (Figures 3 & 4)
    mhr_file, fhr_file = load_accel_decel_data()

    mhr_results = compute_ratios_and_stats(mhr_file, 'maternal')
    fhr_results = compute_ratios_and_stats(fhr_file, 'fetal')

    statistical_tests_accel_decel(mhr_results, fhr_results)

    # Part 2: Hmax/Hmean Analysis (Figures 6 & 7)
    hmax_data, hmean_data = load_hmax_data()
    statistical_tests_hmax(hmax_data, hmean_data)

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
