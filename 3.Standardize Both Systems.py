# ================================================================
#  TASK 3 — Standardize and Cleanse Both Source Systems
#
#  SCENARIO:
#  Before you can merge two systems into a master record you
#  need both systems to speak the same language.
#  Inconsistent casing, formatting differences, and invalid
#  values will cause false mismatches if you do not fix them first.
#  This step is called DATA STANDARDIZATION.
#
#  HOW THIS TASK WORKS:
#  You apply the same cleaning rules to both systems.
#  Each step fixes one category of issue.
#  At the end both systems will be in a consistent format
#  ready for matching and merging.
# ================================================================

import pandas as pd

system_a = pd.read_csv('system_a.csv')
system_b = pd.read_csv('system_b.csv')

print(f"Loaded System A ({len(system_a)} rows) and System B ({len(system_b)} rows)\n")


# ----------------------------------------------------------------
# STEP 1 — Standardize name casing
#
# All first_name and last_name values should be Title Case.
# Some are all lowercase, some are ALL CAPS.
# ----------------------------------------------------------------

for df in [system_a, system_b]:
    df['first_name'] = df['first_name'].str.title()
    df['last_name']  = df['last_name'].str.title()

print(" Name casing standardized")


# ----------------------------------------------------------------
# STEP 2 — Standardize country values
#
# All country values should be 'USA'.
# System B has 'US' and 'usa' mixed in.
# ----------------------------------------------------------------

for df in [system_a, system_b]:
    df['country'] = df['country'].replace({
        'US': 'USA',
        'usa': 'USA'
    })

print("Country values standardized")
print("Unique country values:", system_a['country'].unique(), system_b['country'].unique())
print()


# ----------------------------------------------------------------
# STEP 3 — Standardize phone number format
#
# All phone numbers should follow the format 555-XXXX.
# Some records are missing the hyphen e.g. '5550103'.
# ----------------------------------------------------------------

def fix_phone(phone):
    phone = str(phone).strip()
    
    if '-' not in phone and len(phone) == 7:
        phone = phone[:3] + '-' + phone[3:]
    return phone

for df in [system_a, system_b]:
    df['phone'] = df['phone'].apply(fix_phone)

print("Phone numbers standardized")


# ----------------------------------------------------------------
# STEP 4 — Standardize city casing
#
# Some city values are lowercase e.g. 'houston' instead of 'Houston'.
# Apply Title Case to the city column in both systems.
# ----------------------------------------------------------------

for df in [system_a, system_b]:
    df['city'] = df['city'].str.title()

print("City casing standardized")


# ----------------------------------------------------------------
# STEP 5 — Flag invalid emails
#
# A valid email must contain @ and at least one dot after it.
# TYPE code to add an 'email_valid' column to both DataFrames.
# True if the email looks valid, False if not or if it is blank.
# ----------------------------------------------------------------

for df in [system_a, system_b]:
    df['email_valid'] =  df['email'].str.match(
        r'^[^@]+@[^@]+\.[^@]+$',
        na=False
    )

print("Email validity flagged")
print(f"   System A invalid emails: {(system_a['email_valid'] == False).sum()}")
print(f"   System B invalid emails: {(system_b['email_valid'] == False).sum()}")
print()


# ----------------------------------------------------------------
# STEP 6 — Save the standardized versions
#
# TYPE code to save both cleaned DataFrames as new CSV files:
#   system_a_clean.csv
#   system_b_clean.csv
# ----------------------------------------------------------------

system_a.to_csv('system_a_clean.csv', index=False)
system_b.to_csv('system_b_clean.csv', index=False)


print(" Saved system_a_clean.csv and system_b_clean.csv")
print()
print("SYSTEM A after standardization:")
print(system_a.to_string(index=False))
print()
print("SYSTEM B after standardization:")
print(system_b.to_string(index=False))

