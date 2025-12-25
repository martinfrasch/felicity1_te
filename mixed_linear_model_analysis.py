#!/usr/bin/env python3
"""
Mixed Linear Model Analysis for Figures 3, 4, 6, and 7
Matching methodology from TE/ER/SE analysis (previous session)

Models:
- Accel/Decel: Fraction ~ Sex × Stress × HR_Source × Event_Type + (1|Patient)
- Hmax/Hmean: Value ~ Sex × Stress × Metric × HR_Source × Conditioning + (1|Patient)
"""

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import mixedlm
from statsmodels.stats.multitest import multipletests
import warnings
warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("MIXED LINEAR MODEL ANALYSIS")
print("Figures 3, 4, 6, 7 - Matching TE/ER/SE Methodology")
print("="*80 + "\n")

# ============================================================================
# PART 1: Accel/Decel Ratios - MLM Analysis
# ============================================================================

def load_and_reshape_accel_decel():
    """
    Load accel/decel data and reshape to long format for MLM
    
    Returns: DataFrame with columns:
        Patient_ID, Sex, Stress, HR_Source, Event_Type, Fraction
    """
    
    print("="*80)
    print("PART 1: ACCEL/DECEL RATIOS - DATA PREPARATION")
    print("="*80 + "\n")
    
    # Load data
    mhr_file = np.load('accel_decel_counts_values/accel_deccel_maternalHR_conditioning.npz')
    fhr_file = np.load('accel_decel_counts_values/accel_deccel_fetalHR_conditioning.npz')
    
    # Extract arrays
    n_subjects = len(mhr_file['N_total'])
    
    # Load sex/stress mapping from TE CSV files
    print("Loading sex/stress information from TE files...")
    te_df = pd.read_csv('Nicolas_felicity1/max_TE_mHR_conditioning.csv', 
                        sep=r'\s+', header=None)
    
    # Columns: patient_code, sex (1=male, 0=female), stress (1=stressed, 0=control), all, accel, decel
    sex_stress_map = {}
    for idx, row in te_df.iterrows():
        patient_id = int(row[0])  # Use actual patient code
        sex_stress_map[patient_id] = {
            'Sex': 'male' if row[1] == 1 else 'female',
            'Stress': 'stressed' if row[2] == 1 else 'control'
        }
    
    print(f"Loaded sex/stress for {len(sex_stress_map)} patients\n")
    
    # Create patient ID mapping (TE file may have gaps in patient codes)
    patient_ids = sorted(sex_stress_map.keys())
    
    # Process data
    N_total_mhr = mhr_file['N_total']
    N_accel_mhr = mhr_file['N_accel']
    N_decel_mhr = mhr_file['N_decel']
    
    N_total_fhr = fhr_file['N_total']
    N_accel_fhr = fhr_file['N_accel']
    N_decel_fhr = fhr_file['N_decel']
    
    records = []
    
    for i in range(min(n_subjects, len(patient_ids))):
        patient_id = patient_ids[i]
        
        if patient_id not in sex_stress_map:
            continue
        
        sex = sex_stress_map[patient_id]['Sex']
        stress = sex_stress_map[patient_id]['Stress']
        
        # Maternal HR - Acceleration
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'maternal',
            'Event_Type': 'acceleration',
            'Fraction': N_accel_mhr[i] / N_total_mhr[i]
        })
        
        # Maternal HR - Deceleration
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'maternal',
            'Event_Type': 'deceleration',
            'Fraction': N_decel_mhr[i] / N_total_mhr[i]
        })
        
        # Fetal HR - Acceleration
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'fetal',
            'Event_Type': 'acceleration',
            'Fraction': N_accel_fhr[i] / N_total_fhr[i]
        })
        
        # Fetal HR - Deceleration
        records.append({
            'Patient_ID': patient_id,
            'Sex': sex,
            'Stress': stress,
            'HR_Source': 'fetal',
            'Event_Type': 'deceleration',
            'Fraction': N_decel_fhr[i] / N_total_fhr[i]
        })
    
    df = pd.DataFrame(records)
    
    print(f"Created long-format dataframe:")
    print(f"  Total observations: {len(df)}")
    print(f"  Unique patients: {df['Patient_ID'].nunique()}")
    print(f"  Observations per patient: {len(df) // df['Patient_ID'].nunique()}")
    print(f"\nDistributions:")
    print(f"  Sex: {df.groupby('Sex')['Patient_ID'].nunique().to_dict()}")
    print(f"  Stress: {df.groupby('Stress')['Patient_ID'].nunique().to_dict()}")
    print(f"  HR_Source: {df['HR_Source'].value_counts().to_dict()}")
    print(f"  Event_Type: {df['Event_Type'].value_counts().to_dict()}")
    print(f"\nFirst few rows:")
    print(df.head(8))
    
    return df

def fit_accel_decel_mlm(df):
    """
    Fit mixed linear model for accel/decel data
    
    Model: Fraction ~ Sex × Stress × HR_Source × Event_Type + (1|Patient_ID)
    """
    
    print("\n" + "="*80)
    print("MIXED LINEAR MODEL: ACCEL/DECEL FRACTIONS")
    print("="*80 + "\n")
    
    print("Model specification:")
    print("  Fraction ~ Sex × Stress × HR_Source × Event_Type + (1|Patient_ID)")
    print("  Estimation: REML (restricted maximum likelihood)")
    print(f"  N observations: {len(df)}")
    print(f"  N patients: {df['Patient_ID'].nunique()}\n")
    
    # Fit full model with all 2-way interactions
    # (4-way interaction would be too complex)
    formula = """Fraction ~ C(Sex) + C(Stress) + C(HR_Source) + C(Event_Type) +
                            C(Sex):C(Stress) +
                            C(Sex):C(HR_Source) +
                            C(Sex):C(Event_Type) +
                            C(Stress):C(HR_Source) +
                            C(Stress):C(Event_Type) +
                            C(HR_Source):C(Event_Type)"""
    
    try:
        model = mixedlm(formula, df, groups=df["Patient_ID"], re_formula="1")
        result = model.fit(reml=True, method='lbfgs')
        
        print("="*80)
        print("MODEL RESULTS: ACCEL/DECEL FRACTIONS")
        print("="*80 + "\n")
        print(result.summary())
        
        # Extract and display significant effects
        print("\n" + "="*80)
        print("SIGNIFICANT EFFECTS (p < 0.05)")
        print("="*80 + "\n")
        
        params = result.params
        pvalues = result.pvalues
        stderr = result.bse
        conf_int = result.conf_int()
        
        sig_effects = []
        for param in params.index:
            if param in ['Intercept', 'Group Var']:
                continue
            
            p = pvalues[param]
            sig_mark = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
            
            sig_effects.append({
                'Parameter': param.replace('C(Sex)[T.male]', 'Sex(male)')
                                  .replace('C(Stress)[T.stressed]', 'Stress(stressed)')
                                  .replace('C(HR_Source)[T.maternal]', 'HR_Source(maternal)')
                                  .replace('C(Event_Type)[T.deceleration]', 'Event_Type(deceleration)'),
                'Coef': f"{params[param]:7.4f}",
                'SE': f"{stderr[param]:.4f}",
                'p-value': f"{p:.6f}",
                'Sig': sig_mark
            })
        
        results_df = pd.DataFrame(sig_effects)
        results_df = results_df.sort_values('p-value')
        print(results_df.to_string(index=False))
        
        # Save to CSV
        results_df.to_csv('mlm_accel_decel_results.csv', index=False)
        print("\n✓ Saved to: mlm_accel_decel_results.csv")
        
        return result
        
    except Exception as e:
        print(f"⚠️  Error fitting model: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# PART 2: Hmax/Hmean - MLM Analysis
# ============================================================================

def load_and_reshape_hmax():
    """
    Load hmax/hmean data and reshape to long format for MLM
    """
    
    print("\n\n" + "="*80)
    print("PART 2: HMAX/HMEAN - DATA PREPARATION")
    print("="*80 + "\n")
    
    from pathlib import Path
    
    # Load sex/stress mapping
    te_df = pd.read_csv('Nicolas_felicity1/max_TE_mHR_conditioning.csv', 
                        sep=r'\s+', header=None)
    
    sex_stress_map = {}
    for idx, row in te_df.iterrows():
        patient_id = int(row[0])
        sex_stress_map[patient_id] = {
            'Sex': 'male' if row[1] == 1 else 'female',
            'Stress': 'stressed' if row[2] == 1 else 'control'
        }
    
    patient_ids = sorted(sex_stress_map.keys())
    
    hmax_dir = Path('hmax_hmean_values')
    records = []
    
    # Define conditions
    conditions = [
        ('fetus', 'none', 'fetus_no_conditoning'),
        ('mother', 'none', 'mother_no_conditoning'),
        ('fetus', 'mother_accel', 'fetus_mother_accel'),
        ('fetus', 'mother_decel', 'fetus_mother_decel'),
        ('mother', 'fetus_accel', 'mother_fetus_accel'),
        ('mother', 'fetus_decel', 'mother_fetus_decel'),
    ]
    
    # Load data
    for hr_source, conditioning, filename_key in conditions:
        for metric_type in ['hmax', 'hmean']:
            filepath = hmax_dir / f"{metric_type}_{filename_key}.npz"
            
            if not filepath.exists():
                continue
                
            data = np.load(filepath)
            values = data['all']
            
            for i in range(min(len(values), len(patient_ids))):
                patient_id = patient_ids[i]
                
                if np.isnan(values[i]):
                    continue
                
                records.append({
                    'Patient_ID': patient_id,
                    'Sex': sex_stress_map[patient_id]['Sex'],
                    'Stress': sex_stress_map[patient_id]['Stress'],
                    'Metric': metric_type,
                    'HR_Source': hr_source,
                    'Conditioning': conditioning,
                    'Value': values[i]
                })
    
    df = pd.DataFrame(records)
    
    print(f"Created long-format dataframe:")
    print(f"  Total observations: {len(df)}")
    print(f"  Unique patients: {df['Patient_ID'].nunique()}")
    print(f"  Observations per patient: {len(df) / df['Patient_ID'].nunique():.1f}")
    print(f"\nDistributions:")
    print(f"  Sex: {df.groupby('Sex')['Patient_ID'].nunique().to_dict()}")
    print(f"  Stress: {df.groupby('Stress')['Patient_ID'].nunique().to_dict()}")
    print(f"  Metric: {df['Metric'].value_counts().to_dict()}")
    print(f"  HR_Source: {df['HR_Source'].value_counts().to_dict()}")
    print(f"  Conditioning: {df['Conditioning'].value_counts().to_dict()}")
    
    print("\n⚠️  DATA QUALITY NOTE:")
    print("  Stressed/Control may contain identical data (flagged issue)")
    
    return df

def fit_hmax_mlm(df):
    """Fit mixed linear model for hmax/hmean data"""
    
    print("\n" + "="*80)
    print("MIXED LINEAR MODEL: HMAX/HMEAN VALUES")
    print("="*80 + "\n")
    
    print("Model specification:")
    print("  Value ~ Sex × Stress × Metric × HR_Source × Conditioning + (1|Patient_ID)")
    print("  (with selected 2-way interactions)")
    print(f"  N observations: {len(df)}")
    print(f"  N patients: {df['Patient_ID'].nunique()}\n")
    
    # Simplified model with key 2-way interactions
    formula = """Value ~ C(Sex) + C(Stress) + C(Metric) + C(HR_Source) + C(Conditioning) +
                        C(Sex):C(Stress) +
                        C(Sex):C(HR_Source) +
                        C(Sex):C(Conditioning) +
                        C(Metric):C(HR_Source) +
                        C(Metric):C(Conditioning)"""
    
    try:
        model = mixedlm(formula, df, groups=df["Patient_ID"], re_formula="1")
        result = model.fit(reml=True, method='lbfgs')
        
        print("="*80)
        print("MODEL RESULTS: HMAX/HMEAN")
        print("="*80 + "\n")
        print(result.summary())
        
        # Extract significant effects
        print("\n" + "="*80)
        print("SIGNIFICANT EFFECTS (p < 0.05)")
        print("="*80 + "\n")
        
        params = result.params
        pvalues = result.pvalues
        stderr = result.bse
        
        sig_effects = []
        for param in params.index:
            if param in ['Intercept', 'Group Var']:
                continue
            
            p = pvalues[param]
            sig_mark = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'ns'
            
            sig_effects.append({
                'Parameter': param.replace('C(Sex)[T.male]', 'Sex(male)')
                                  .replace('C(Stress)[T.stressed]', 'Stress(stressed)')
                                  .replace('C(Metric)[T.hmean]', 'Metric(hmean)')
                                  .replace('C(HR_Source)[T.mother]', 'HR_Source(mother)')
                                  .replace('C(Conditioning)', 'Cond'),
                'Coef': f"{params[param]:7.4f}",
                'SE': f"{stderr[param]:.4f}",
                'p-value': f"{p:.6f}",
                'Sig': sig_mark
            })
        
        results_df = pd.DataFrame(sig_effects)
        results_df = results_df.sort_values('p-value')
        print(results_df.to_string(index=False))
        
        # Save to CSV
        results_df.to_csv('mlm_hmax_hmean_results.csv', index=False)
        print("\n✓ Saved to: mlm_hmax_hmean_results.csv")
        
        return result
        
    except Exception as e:
        print(f"⚠️  Error fitting model: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run complete MLM analysis"""
    
    # Part 1: Accel/Decel
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*15 + "PART 1: ACCELERATION/DECELERATION RATIOS" + " "*23 + "║")
    print("╚" + "="*78 + "╝")
    
    df_accel = load_and_reshape_accel_decel()
    result_accel = fit_accel_decel_mlm(df_accel)
    
    if result_accel:
        df_accel.to_csv('mlm_accel_decel_data.csv', index=False)
        print(f"\n✓ Saved data to: mlm_accel_decel_data.csv")
    
    # Part 2: Hmax/Hmean
    print("\n\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "PART 2: HMAX/HMEAN ENTROPY RATE" + " "*26 + "║")
    print("╚" + "="*78 + "╝")
    
    df_hmax = load_and_reshape_hmax()
    result_hmax = fit_hmax_mlm(df_hmax)
    
    if result_hmax:
        df_hmax.to_csv('mlm_hmax_hmean_data.csv', index=False)
        print(f"\n✓ Saved data to: mlm_hmax_hmean_data.csv")
    
    # Summary
    print("\n\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nFiles generated:")
    print("  1. mlm_accel_decel_data.csv - Reshaped data")
    print("  2. mlm_accel_decel_results.csv - MLM results table")
    print("  3. mlm_hmax_hmean_data.csv - Reshaped data")
    print("  4. mlm_hmax_hmean_results.csv - MLM results table")
    print("  5. mlm_analysis_results.txt - Full output log")
    print("\nTo re-run with corrected hmax/hmean data:")
    print("  python3 mixed_linear_model_analysis.py")
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()
