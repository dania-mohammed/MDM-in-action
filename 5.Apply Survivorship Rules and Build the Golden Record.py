# ================================================================
#  TASK 5 — Apply Survivorship Rules and Build the Golden Record
#  Master Data Management — Udemy Practice Lab
#
#  SCENARIO:
#  You have matched records across both systems.
#  Now comes the most important decision in MDM:
#  when two systems disagree on a value, which one wins?
#
#  These decisions are called SURVIVORSHIP RULES.
#  They define which source is trusted for each attribute.
#  Once applied, the result is called the GOLDEN RECORD:
#  one authoritative master record per customer.
#
#  HOW THIS TASK WORKS:
#  You will define survivorship rules for each column and
#  apply them to produce a single clean row per customer.
# ================================================================

import pandas as pd

email_matches      = pd.read_csv('email_matches.csv')
name_phone_matches = pd.read_csv('name_phone_matches.csv')
unmatched_a        = pd.read_csv('unmatched_a.csv')
unmatched_b        = pd.read_csv('unmatched_b.csv')
system_a           = pd.read_csv('system_a_clean.csv')
system_b           = pd.read_csv('system_b_clean.csv')

print("Match data loaded\n")


# ----------------------------------------------------------------
# STEP 1 — Define your survivorship rules
#
# For each attribute, decide which system wins when they conflict.
# These rules should reflect business logic, not guesswork.
#
# Read these rules and TYPE your understanding of why each
# one makes sense as a comment next to each rule.
#
# Then we will apply them in Steps 2 and 3.
# ----------------------------------------------------------------

survivorship_rules = {
    'first_name'   : 'System A',   # Why? TYPE HERE
    'last_name'    : 'System A',   # Why? TYPE HERE
    'email'        : 'System A',   # Why? TYPE HERE
    'phone'        : 'System A',   # Why? TYPE HERE
    'city'         : 'Most Recent',# Why? TYPE HERE
    'country'      : 'System A',   # Why? TYPE HERE
    'segment'      : 'System A',   # Why? TYPE HERE
    'annual_spend' : 'Highest',    # Why? TYPE HERE
}

print(" Survivorship Rules:")
for col, rule in survivorship_rules.items():
    print(f"   {col:<15} : {rule}")
print()


# ----------------------------------------------------------------
# STEP 2 — Apply survivorship rules to email matched pairs
#
# For each matched pair apply the rules above to pick one value.
#
# TYPE a function called build_golden_record(row) that takes
# a row from email_matches and returns a dict with the
# surviving value for each column based on the rules above.
#
# Rules to apply:
#   System A   = always use the _A version
#   Most Recent = use whichever system has the later last_updated
#   Highest     = use whichever system has the higher number
#
#    "Write a Python function that takes a pandas
#               row with columns ending in _A and _B and
#               returns a dictionary selecting values based
#               on three rules: prefer A, prefer most recent
#               date, and prefer the highest number."
# ----------------------------------------------------------------

def build_golden_record(row):
    record = {}

    # System A wins fields
    record['first_name'] = row['first_name_A']
    record['last_name']  = row['last_name_A']
    record['email']      = row['email']          # same for both in email match
    record['phone']      = row['phone_A']
    record['country']    = row['country_A']
    record['segment']    = row['segment_A']

    # Most Recent wins (compare dates)
    if row['last_updated_A'] > row['last_updated_B']:
        record['city'] = row['city_A']
        record['last_updated'] = row['last_updated_A']
    else:
        record['city'] = row['city_B']
        record['last_updated'] = row['last_updated_B']

    # Highest wins
    record['annual_spend'] = max(row['annual_spend_A'], row['annual_spend_B'])

    return record
   

golden_from_matches = email_matches.apply(build_golden_record, axis=1, result_type='expand')
golden_from_matches['match_id'] = email_matches['match_id'].values
golden_from_matches['source']   = 'MERGED'

print(f"Golden records built from email matches: {len(golden_from_matches)}")
print(golden_from_matches.to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 3 — Add unmatched records as-is
#
# Records that only exist in one system need no merging.
# They go straight into the master table as their own
# golden record.
#
# TYPE code to:
#   1. Take unmatched_a rows and select only the columns
#      that match your golden record structure
#   2. Do the same for unmatched_b
#   3. Add a 'source' column showing 'A_ONLY' or 'B_ONLY'
# ----------------------------------------------------------------

cols = ['first_name','last_name','email','phone','city',
        'country','segment','annual_spend']

golden_a_only = unmatched_a[cols].copy()
golden_a_only['source']   = 'A_ONLY'
golden_a_only['match_id'] = [
    f"MATCH{str(i+1+len(email_matches)+len(name_phone_matches)).zfill(3)}"
    for i in range(len(golden_a_only))
]

golden_b_only = unmatched_b[cols].copy()
golden_b_only['source']   = 'B_ONLY'
golden_b_only['match_id'] = [
    f"MATCH{str(i+1+len(email_matches)+len(name_phone_matches)+len(golden_a_only)).zfill(3)}"
    for i in range(len(golden_b_only))
]

print(f"Unique System A records: {len(golden_a_only)}")
print(f"Unique System B records: {len(golden_b_only)}")
print()


# ----------------------------------------------------------------
# STEP 4 — Combine into the final master table
#
# TYPE code to concatenate:
#   golden_from_matches + golden_a_only + golden_b_only
# into one DataFrame called master_df.
#
# Then add a master_id column with values MDM001, MDM002 etc.
# ----------------------------------------------------------------

master_df = pd.concat(
    [golden_from_matches, golden_a_only, golden_b_only],
    ignore_index=True
)

master_df['master_id'] =  [
    f"MDM{str(i+1).zfill(3)}"
    for i in range(len(master_df))
]

print(f"MASTER TABLE: {len(master_df)} golden records")
print(master_df.to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 5 — Save the master table
#
# TYPE code to save master_df as master_customers.csv
# ----------------------------------------------------------------

master_df.to_csv('master_customers.csv', index=False)

print(" master_customers.csv saved")
print("   Every customer now has exactly one master record.")

