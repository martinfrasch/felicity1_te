"""
Verify Group Assignments Between Excel and NPZ Files
Checks if the group assignments in the .npz files match the groups_scores_new.xlsx
"""

import numpy as np
import pandas as pd
from pathlib import Path

# Paths
DATA_DIR = Path("/Users/mfrasch/Library/CloudStorage/GoogleDrive-mg@frasch.ca/My Drive/Cloud work/Nicolas Garnier/FELICITy1_TE_paper/TE_ER_data")
EXCEL_FILE = Path("/Users/mfrasch/Library/CloudStorage/GoogleDrive-mg@frasch.ca/My Drive/Cloud work/Nicolas Garnier/FELICITy1_TE_paper/groups_scores_new.xlsx")
ENTROPY_RATE_FILE = Path("/Users/mfrasch/Library/CloudStorage/GoogleDrive-mg@frasch.ca/My Drive/Cloud work/Nicolas Garnier/FELICITy1_TE_paper/entropy_rate.txt")

print("="*100)
print("GROUP ASSIGNMENT VERIFICATION")
print("="*100)

# Step 1: Extract patient IDs from entropy_rate.txt
print("\nStep 1: Extracting patient IDs from entropy_rate.txt...")
patient_ids_numeric = []
with open(ENTROPY_RATE_FILE, 'r') as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            patient_ids_numeric.append(int(parts[0]))

patient_ids_numeric = sorted(set(patient_ids_numeric))
patient_ids_fs = [f'FS-{pid:03d}' for pid in patient_ids_numeric]

print(f"  Found {len(patient_ids_numeric)} unique patients")
print(f"  First 10: {patient_ids_fs[:10]}")

# Step 2: Load Excel file and get group assignments
print("\nStep 2: Loading Excel file and matching patients...")
df_excel = pd.read_excel(EXCEL_FILE)

# Match patients
matched_patients = []
for fs_id in patient_ids_fs:
    if fs_id in df_excel['Patient'].values:
        group = df_excel[df_excel['Patient'] == fs_id]['Group'].values[0]
        matched_patients.append({'Patient': fs_id, 'Group': group})
    else:
        print(f"  WARNING: {fs_id} not found in Excel file")
        matched_patients.append({'Patient': fs_id, 'Group': np.nan})

df_matched = pd.DataFrame(matched_patients)

# Count groups
group_counts = df_matched[~df_matched['Group'].isna()]['Group'].value_counts().sort_index()
print(f"\n  Matched patients: {len(df_matched[~df_matched['Group'].isna()])}")
print(f"  Control (Group 0): {group_counts.get(0, 0)}")
print(f"  Stressed (Group 1): {group_counts.get(1, 0)}")

# Step 3: Load a representative .npz file to check group assignments
print("\nStep 3: Loading .npz file to check current group assignments...")

# Use a file that has different values for stressed/control (not the "no conditioning" files)
npz_file = DATA_DIR / "TEmax_fetus_accel.npz"
data = np.load(npz_file)

print(f"\n  Loaded: {npz_file.name}")
print(f"  Arrays in file: {data.files}")
print(f"\n  Current array sizes:")
for key in ['all', 'stressed', 'control', 'male', 'female']:
    if key in data.files:
        print(f"    {key}: {len(data[key])}")

# Step 4: Check if group assignments are consistent
print("\n" + "="*100)
print("VERIFICATION RESULTS")
print("="*100)

# Expected from Excel
expected_total = len(df_matched[~df_matched['Group'].isna()])
expected_control = int(group_counts.get(0, 0))
expected_stressed = int(group_counts.get(1, 0))

# Actual from .npz
actual_total = len(data['all']) if 'all' in data.files else 0
actual_control = len(data['control']) if 'control' in data.files else 0
actual_stressed = len(data['stressed']) if 'stressed' in data.files else 0

print(f"\nExpected (from Excel matching):")
print(f"  Total: {expected_total}")
print(f"  Control: {expected_control}")
print(f"  Stressed: {expected_stressed}")

print(f"\nActual (from .npz file):")
print(f"  Total: {actual_total}")
print(f"  Control: {actual_control}")
print(f"  Stressed: {actual_stressed}")

print(f"\nComparison:")
if actual_total == expected_total:
    print(f"  ✓ Total matches")
else:
    print(f"  ✗ Total MISMATCH (expected {expected_total}, got {actual_total})")
    print(f"    Difference: {actual_total - expected_total} patients")

if actual_control == expected_control:
    print(f"  ✓ Control group matches")
else:
    print(f"  ✗ Control group MISMATCH (expected {expected_control}, got {actual_control})")
    print(f"    Difference: {actual_control - expected_control} patients")

if actual_stressed == expected_stressed:
    print(f"  ✓ Stressed group matches")
else:
    print(f"  ✗ Stressed group MISMATCH (expected {expected_stressed}, got {actual_stressed})")
    print(f"    Difference: {actual_stressed - expected_stressed} patients")

# Step 5: Create mapping for verification
print("\n" + "="*100)
print("PATIENT LISTING BY GROUP")
print("="*100)

control_patients_excel = df_matched[df_matched['Group'] == 0]['Patient'].tolist()
stressed_patients_excel = df_matched[df_matched['Group'] == 1]['Patient'].tolist()

print(f"\nControl patients from Excel (n={len(control_patients_excel)}):")
print(f"  First 20: {control_patients_excel[:20]}")

print(f"\nStressed patients from Excel (n={len(stressed_patients_excel)}):")
print(f"  First 20: {stressed_patients_excel[:20]}")

# Save mapping to CSV for future reference
mapping_df = df_matched.copy()
mapping_df['Expected_Group'] = mapping_df['Group']
mapping_df.to_csv('patient_group_mapping.csv', index=False)
print(f"\n✓ Patient-group mapping saved to: patient_group_mapping.csv")

# Step 6: Recommendations
print("\n" + "="*100)
print("RECOMMENDATIONS")
print("="*100)

if actual_control != expected_control or actual_stressed != expected_stressed:
    print("""
The group assignments in the .npz files DO NOT match the Excel file.

CRITICAL ISSUE: There is a discrepancy between:
  - Excel file (groups_scores_new.xlsx): {ec} control, {es} stressed
  - NPZ files: {ac} control, {stressed_actual} stressed

This means the statistical analysis may have used INCORRECT group assignments.

NEXT STEPS:
1. Verify which source is correct (Excel file or .npz files)
2. If Excel is correct, regenerate .npz files with correct group assignments
3. Re-run statistical analysis with corrected groups
4. Check if there's documentation about how .npz files were created

ALTERNATIVE: The .npz files might have been created with balanced groups (58/58)
by excluding some patients from the Excel file. We need to identify WHICH
patients were included in the .npz files to verify the group assignments.
""".format(ec=expected_control, es=expected_stressed, ac=actual_control, stressed_actual=actual_stressed))
else:
    print("""
✓ Group assignments appear consistent between Excel and .npz files.

However, we still need to verify that the SAME patients are in both sources.
The entropy_rate.txt file suggests there are 120 patients, but we can only
match 119 to the Excel file (FS-004 is missing).

NEXT STEP: Create a complete patient-level dataset that includes:
  - Patient ID
  - Group assignment from Excel
  - TE/ER values from .npz files
This will allow us to verify the analysis at the patient level.
""")
