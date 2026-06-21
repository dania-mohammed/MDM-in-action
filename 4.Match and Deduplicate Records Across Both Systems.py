# ================================================================
#  TASK 4 — Match and Deduplicate Records Across Both Systems
#  SCENARIO:
#  You now have two clean standardized systems.
#  The next step is RECORD MATCHING: figuring out which records
#  in System A and System B represent the same real customer.
#
#  In MDM this is called ENTITY RESOLUTION.
#  The goal is to group records that belong to the same person
#  so you can later merge them into one master record.
#
#  HOW THIS TASK WORKS:
#  You will match records using two strategies:
#    1. Exact match on email (high confidence)
#    2. Name plus phone match (medium confidence)
#  Anything that does not match is treated as a unique new record.
# ================================================================

import pandas as pd

system_a = pd.read_csv('system_a_clean.csv')
system_b = pd.read_csv('system_b_clean.csv')

print(f"✅ Loaded cleaned systems\n")


# ----------------------------------------------------------------
# STEP 1 — Exact match on email
#
# Records with the same email address in both systems are
# almost certainly the same customer.
#
# TYPE code to find rows from system_a and system_b
# that share the same email address.
# Merge them together with suffixes _A and _B.
# Store the result in a DataFrame called email_matches.
# ----------------------------------------------------------------

email_matches = pd.merge(
    system_a[system_a['email_valid'] == True],
    system_b[system_b['email_valid'] == True],
    on     = 'email',
    how    = 'inner',
    suffixes = ('_A', '_B')
)

print(f"Records matched by email: {len(email_matches)}")
print(email_matches[['email','first_name_A','first_name_B','city_A','city_B','annual_spend_A','annual_spend_B']].to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 2 — Find unmatched records from each system
#
# Records that did NOT match on email are either:
#   a) Genuinely unique customers only in one system
#   b) The same customer with a different or missing email
#
# TYPE code to find:
#   unmatched_a = system_a rows whose email is NOT in email_matches
#   unmatched_b = system_b rows whose email is NOT in email_matches
# ----------------------------------------------------------------

matched_emails = set(email_matches['email'])

unmatched_a = system_a[~system_a['email'].isin(matched_emails)]
unmatched_b = system_b[~system_b['email'].isin(matched_emails)]

print(f"Unmatched records in System A: {len(unmatched_a)}")
print(unmatched_a[['source_id','first_name','last_name','email','phone']].to_string(index=False))
print()
print(f"Unmatched records in System B: {len(unmatched_b)}")
print(unmatched_b[['source_id','first_name','last_name','email','phone']].to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 3 — Secondary match on name and phone
#
# For unmatched records, try matching on first_name + last_name
# + phone. This catches cases where the email was different
# or missing but the person is still the same.
#
# TYPE code to merge unmatched_a and unmatched_b on:
#   first_name, last_name, and phone
# Store the result in name_phone_matches.
# ----------------------------------------------------------------

name_phone_matches = pd.merge(
    unmatched_a,
    unmatched_b,
    on       = ['first_name', 'last_name', 'phone'],
    how      = 'inner',
    suffixes = ('_A','_B')
)

print(f"Additional matches by name and phone: {len(name_phone_matches)}")
if len(name_phone_matches) > 0:
    print(name_phone_matches[['first_name','last_name','phone','email_A','email_B']].to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 4 — Assign a match group ID to each matched pair
#
# Every matched pair needs a shared ID so we know they belong
# together when we build the golden record in Task 5.
#
# TYPE code to:
#   1. Take email_matches and add a column 'match_id'
#      with values like 'MATCH001', 'MATCH002' etc.
#   2. Do the same for name_phone_matches
#   3. Print both with their match IDs
# ----------------------------------------------------------------

email_matches = email_matches.copy()
name_phone_matches = name_phone_matches.copy()

email_matches['match_id']       = [
    f"MATCH{str(i+1).zfill(3)}"
    for i in range(len(email_matches))
]

name_phone_matches['match_id']  =  [
    f"MATCH{str(i+1+len(email_matches)).zfill(3)}"
    for i in range(len(name_phone_matches))
]


print("Email matches with match IDs:")
print(email_matches[['match_id','email','source_id_A','source_id_B']].to_string(index=False))
print()

print("Name + phone matches with match IDs:")
print(name_phone_matches[['match_id','first_name','last_name','phone']].to_string(index=False))
print()

# ----------------------------------------------------------------
# STEP 5 — Save the match results
#
# TYPE code to save:
#   email_matches        as  email_matches.csv
#   name_phone_matches   as  name_phone_matches.csv
#   unmatched_a          as  unmatched_a.csv
#   unmatched_b          as  unmatched_b.csv
# ----------------------------------------------------------------

email_matches.to_csv('email_matches.csv', index=False)
name_phone_matches.to_csv('name_phone_matches.csv', index=False)
unmatched_a.to_csv('unmatched_a.csv', index=False)
unmatched_b.to_csv('unmatched_b.csv', index=False)


print(" Match results saved")
print(f"\n   Summary:")
print(f"   Matched by email         : {len(email_matches)}")
print(f"   Matched by name/phone    : {len(name_phone_matches)}")
print(f"   Unique to System A only  : {len(unmatched_a) - len(name_phone_matches)}")
print(f"   Unique to System B only  : {len(unmatched_b) - len(name_phone_matches)}")


