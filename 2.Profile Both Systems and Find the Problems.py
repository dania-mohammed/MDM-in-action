# ================================================================
#  This is called SOURCE PROFILING and it is the first step
#  in every real MDM project.
# ================================================================

import pandas as pd

system_a = pd.read_csv('system_a.csv')
system_b = pd.read_csv('system_b.csv')
df       = pd.read_csv('customers_raw.csv')

print(f"Loaded {len(df)} records across both systems\n")


# ----------------------------------------------------------------
# STEP 1 — Check for missing values in each system
# ----------------------------------------------------------------

print("Missing values in System A:")
print(system_a.isnull().sum())

print("\nMissing values in System B:")
print(system_b.isnull().sum())
print()


# ----------------------------------------------------------------
# STEP 2 — Find records that exist in BOTH systems
# ----------------------------------------------------------------

emails_a        = set(system_a.loc[system_a['email'] != '', 'email'])
emails_b        = set(system_b.loc[system_b['email'] != '', 'email'])
matching_emails = emails_a & emails_b

print(f"Customers found in BOTH systems: {len(matching_emails)}")
print(matching_emails)
print()


# ----------------------------------------------------------------
# STEP 3 — Find conflicting values for matched customers
# ----------------------------------------------------------------

a_matched = system_a[system_a['email'].isin(matching_emails)]
b_matched = system_b[system_b['email'].isin(matching_emails)]

conflicts = pd.merge(
    a_matched[['email','first_name','last_name','city','country','annual_spend','last_updated']],
    b_matched[['email','first_name','last_name','city','country','annual_spend','last_updated']],
    on='email',
    suffixes=('_A','_B')
)

print("Conflicting values for matched customers:")
print(conflicts.to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 4 — Check for formatting inconsistencies
# ----------------------------------------------------------------
# Country values not equal to USA
bad_country = df[df['country'] != 'USA']
# Phone numbers not containing a hyphen
bad_phone   = df[~df['phone'].str.contains('-', na=False)]
# First names not in Title Case
bad_names   = df[df['first_name'] != df['first_name'].str.title()]

print(f"Inconsistent country values : {len(bad_country)}")
print(bad_country[['source','source_id','country']])
print()
print(f"Inconsistent phone formats  : {len(bad_phone)}")
print(bad_phone[['source','source_id','phone']])
print()
print(f"Inconsistent name casing    : {len(bad_names)}")
print(bad_names[['source','source_id','first_name']])
print()


# ----------------------------------------------------------------
# STEP 5 — Summarize your findings
# ----------------------------------------------------------------
total_records = len(df)

duplicate_customers = len(matching_emails)

missing_email = df['email'].isna().sum() + (df['email'].astype(str).str.strip() == '').sum()

missing_phone = df['phone'].isna().sum() + (df['phone'].astype(str).str.strip() == '').sum()

formatting_issues = len(bad_country) + len(bad_phone) + len(bad_names)
print(" SOURCE PROFILING SUMMARY:")
print("""
Total records analyzed: {total_records}

Duplicate customers found across systems: {duplicate_customers}

Records with missing email addresses: {missing_email}
Records with missing phone numbers: {missing_phone}

Country formatting issues: {len(bad_country)}
Phone formatting issues: {len(bad_phone)}
Name casing issues: {len(bad_names)}

Total formatting issues identified: {formatting_issues}

Source Profiling Assessment:
The analysis of the two CRM systems identified several master data quality
issues requiring remediation before creating a trusted customer master.
Six customers were found to exist in both systems, indicating duplicate
customer records that must be matched and merged. Data quality issues
include missing email addresses, inconsistent country values (US/usa vs USA),
non-standard phone number formats, and inconsistent name capitalization.

Additionally, conflicting attribute values were detected between systems
for several duplicate customers, including differences in annual spend,
country values, and customer names. These conflicts will require
survivorship rules to determine the golden record.

Overall, the source systems contain duplicate, incomplete, and inconsistent
customer data, making data cleansing, standardization, matching, and
survivorship necessary before loading records into an MDM hub.
""")


