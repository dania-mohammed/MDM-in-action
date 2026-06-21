# ================================================================
#  TASK 6 — Validate the Master Data and Build a Lineage Map
# 
#
#  SCENARIO:
#  You have a master table. But how do you know it is correct?
#  In MDM, every golden record must be validated against
#  business rules before it is trusted as the source of truth.
#
#  You also need to document WHERE each record came from.
#  This is called DATA LINEAGE and it is a core requirement
#  in any production MDM system.
#
#  HOW THIS TASK WORKS:
#  You apply validation rules to the master table.
#  Then you build a lineage map that traces each master record
#  back to its original source system records.
# ================================================================

import pandas as pd

master_df = pd.read_csv('master_customers.csv')
system_a  = pd.read_csv('system_a_clean.csv')
system_b  = pd.read_csv('system_b_clean.csv')

print(f"Master table loaded: {len(master_df)} records\n")


# ----------------------------------------------------------------
# STEP 1 — Validate master IDs are unique
#
# Every master_id must be unique. No exceptions.
#
# TYPE code to check whether any master_id appears more than once.
# Print the count. It must be zero.
# ----------------------------------------------------------------

duplicate_master_ids = master_df['master_id'].duplicated().sum()
print(f"Duplicate master IDs: {duplicate_master_ids}  ({'PASS' if duplicate_master_ids == 0 else 'FAIL'})")


# ----------------------------------------------------------------
# STEP 2 — Validate no critical fields are blank
#
# A golden record must have at minimum:
#   first_name, last_name, and either email or phone
#
# TYPE code to find any master records that are missing
# both email AND phone at the same time.
# ----------------------------------------------------------------

no_contact = master_df[
        (
        master_df['email'].fillna('').str.strip() == ''
    ) &
    (
        master_df['phone'].fillna('').str.strip() == ''
    )
]
print(f"Records with no email and no phone: {len(no_contact)}  ({'PASS' if len(no_contact) == 0 else 'FAIL'})")
if len(no_contact) > 0:
    print(no_contact[['master_id','first_name','last_name','email','phone']].to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 3 — Validate annual_spend is a positive number
#
# TYPE code to find any master records where annual_spend
# is missing, zero, or negative.
# ----------------------------------------------------------------

bad_spend = master_df[
        master_df['annual_spend'].isna() |
    (master_df['annual_spend'] <= 0)
]
print(f"Records with invalid annual spend: {len(bad_spend)}  ({'PASS' if len(bad_spend) == 0 else 'FAIL'})")
print()


# ----------------------------------------------------------------
# STEP 4 — Validate segment values are from the approved list
#
# Approved segments are: Enterprise, SMB, Startup
# TYPE code to find any master records with a segment value
# outside of this list.
# ----------------------------------------------------------------

valid_segments  = ['Enterprise', 'SMB', 'Startup']
invalid_segment = ~master_df['segment'].isin(valid_segments)

print(f"Records with invalid segment: {len(invalid_segment)}  ({'PASS' if len(invalid_segment) == 0 else 'FAIL'})")
print()


# ----------------------------------------------------------------
# STEP 5 — Build the data lineage map
#
# A lineage map shows which source system records contributed
# to each master record. It answers the question:
# "Where did this data come from?"
#
# TYPE code to create a lineage DataFrame with columns:
#   master_id | source_system | source_id | contributed_fields
#
# For MERGED records: both A and B contributed
# For A_ONLY records: only System A contributed
# For B_ONLY records: only System B contributed
#
#   "Write Python code that loops through a pandas
#               DataFrame and builds a new lineage DataFrame
#               based on a source column that has values
#               MERGED, A_ONLY, and B_ONLY."
# ----------------------------------------------------------------

lineage_rows = []

for _, row in master_df.iterrows():
    if row['source'] == 'MERGED':

        lineage_rows.append({
            'master_id': row['master_id'],
            'source_system': 'System A',
            'source_id': row['source_id_A'],
            'contributed_fields': 'first_name,last_name,email,phone,country,segment'
        })
        lineage_rows.append({
            'master_id': row['master_id'],
            'source_system': 'System B',
            'source_id': row['source_id_B'],
            'contributed_fields': 'city,annual_spend'
        })


       
    elif row['source'] == 'A_ONLY':
        lineage_rows.append({
            'master_id': row['master_id'],
            'source_system': 'System A',
            'source_id': row['source_id'],
            'contributed_fields': 'ALL'
        })

    elif row['source'] == 'B_ONLY':
        lineage_rows.append({
            'master_id': row['master_id'],
            'source_system': 'System B',
            'source_id': row['source_id'],
            'contributed_fields': 'ALL'
        })

lineage_df = pd.DataFrame(lineage_rows)

print("DATA LINEAGE MAP (first 15 rows):")
print(lineage_df.head(15).to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 6 — Save the validation report and lineage map
#
# TYPE code to save lineage_df as lineage_map.csv
# Then print a validation summary showing pass or fail
# for each rule you checked.
# ----------------------------------------------------------------

lineage_df.to_csv('lineage_map.csv', index=False)

print(" VALIDATION SUMMARY:")
print(f"  Unique master IDs     : {'PASS' if duplicate_master_ids == 0 else 'FAIL'}")
print(f"  No missing contact    : {'PASS' if len(no_contact) == 0 else 'FAIL'}")
print(f"  Valid annual spend    : {'PASS' if len(bad_spend) == 0 else 'FAIL'}")
print(f"  Valid segment values  : {'PASS' if len(invalid_segment) == 0 else 'FAIL'}")
print()
print(" lineage_map.csv saved")

