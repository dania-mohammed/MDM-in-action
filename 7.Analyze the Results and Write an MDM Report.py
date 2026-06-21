# ================================================================
#  TASK 7 — Analyze the Master Data and Write an MDM Report
#
#  SCENARIO:
#  The MDM project is complete. You have a validated golden
#  record table and a full lineage map.
#  Now the data governance team needs a report that explains
#  what was done, what was found, and what the master data
#  looks like.
#
#  This is the deliverable that justifies the MDM project
#  to leadership. It needs to be clear, factual, and
#  supported by numbers and visuals.
#
#  HOW THIS TASK WORKS:
#  You calculate the key MDM metrics yourself.
#  You build two charts.
#  Then you write the report narrative.
#  You save everything as a final report file.
# ================================================================

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

master_df  = pd.read_csv('master_customers.csv')
lineage_df = pd.read_csv('lineage_map.csv')
system_a   = pd.read_csv('system_a_clean.csv')
system_b   = pd.read_csv('system_b_clean.csv')

print(f"All files loaded\n")


# ----------------------------------------------------------------
# STEP 1 — Calculate your MDM project metrics
#
# TYPE each calculation. These are the numbers that go
# into your report.
# ----------------------------------------------------------------

total_source_records  = len(system_a) + len(system_b)
total_master_records  = len(master_df)
records_merged        = len(master_df[master_df['source'] == 'MERGED'])
records_a_only        = len(master_df[master_df['source'] == 'A_ONLY'])
records_b_only        = len(master_df[master_df['source'] == 'B_ONLY'])
dedup_rate            = (
     (total_source_records - total_master_records)
    / total_source_records
    ) * 100

print(" MDM PROJECT METRICS:")
print(f"  Total source records   : {total_source_records}")
print(f"  Total master records   : {total_master_records}")
print(f"  Merged (both systems)  : {records_merged}")
print(f"  System A only          : {records_a_only}")
print(f"  System B only          : {records_b_only}")
print(f"  Deduplication rate     : {dedup_rate:.1f}%")
print()


# ----------------------------------------------------------------
# STEP 2 — Analyze the master data by segment
#
# TYPE a groupby on master_df that shows per segment:
#   number of customers and total annual spend
# Sort by total spend descending.
# ----------------------------------------------------------------

segment_summary = (
    master_df
    .groupby('segment')
    .agg(
        customer_count=('master_id', 'count'),
        total_annual_spend=('annual_spend', 'sum')
    )
    .reset_index()
    .sort_values('total_annual_spend', ascending=False)
)


print("Master Data by Segment:")
print(segment_summary.to_string(index=False))
print()


# ----------------------------------------------------------------
# STEP 3 — Chart 1: Record origin breakdown (pie chart)
#
# TYPE a pie chart showing how many records came from:
#   Merged, System A Only, System B Only
#
# "Write matplotlib code for a pie chart from
#               three values with labels and percentage display."
#
# Save as: chart_record_origin.png
# ----------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

labels = ['Merged', 'System A Only', 'System B Only']
sizes = [records_merged, records_a_only, records_b_only]

ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90
)

ax.set_title('MDM Record Origin Breakdown')

plt.savefig('chart_record_origin.png', bbox_inches='tight')
plt.show()
print(" Saved chart_record_origin.png")


# ----------------------------------------------------------------
# STEP 4 — Chart 2: Annual spend by customer segment (bar chart)
#
# TYPE a bar chart from segment_summary showing segment on the
# x axis and total annual spend on the y axis.
# Add value labels on top of each bar.
#
# Save as: chart_spend_by_segment.png
# ----------------------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(segment_summary['segment'], segment_summary['annual_spend'])

ax.set_title('Annual Spend by Customer Segment')
ax.set_xlabel('Customer Segment')
ax.set_ylabel('Total Annual Spend')

# Add value labels on top of bars
for i, value in enumerate(segment_summary['annual_spend']):
    ax.text(i, value, str(value), ha='center', va='bottom')

plt.savefig('chart_spend_by_segment.png', bbox_inches='tight')
plt.show()
print("Saved chart_spend_by_segment.png")
print()


# ----------------------------------------------------------------
# STEP 5 — Write the MDM report using AI
#
#   "Write an MDM project completion report with 4 sections:
#
#    PROJECT OVERVIEW: what the project involved and why it was done
#    WHAT WAS FOUND: the data quality and duplication issues discovered
#    WHAT WAS DONE: the standardization, matching, and merging steps
#    MASTER DATA SUMMARY: the final state of the customer master table
#
#    Use these numbers:
#    - Source records: [total_source_records] across 2 systems
#    - Master records after deduplication: [total_master_records]
#    - Deduplication rate: [dedup_rate]%
#    - Merged records (appeared in both systems): [records_merged]
#    - Enterprise customers: [n] with total spend $[amount]
#    - SMB customers: [n] with total spend $[amount]
#    - Startup customers: [n] with total spend $[amount]
#
#    Audience: data governance team and business leadership.
#    Tone: professional and factual.
#    Length: under 350 words."

# ----------------------------------------------------------------

ai_report = """
MDM PROJECT COMPLETION REPORT

PROJECT OVERVIEW:
This project focused on implementing a Master Data Management (MDM) process to consolidate customer data from two independent CRM systems (System A and System B). The objective was to create a single, trusted source of truth for customer information by identifying duplicates, resolving inconsistencies, and generating unified golden records for analytical and operational use.

WHAT WAS FOUND:
The initial data profiling revealed significant quality issues, including duplicate customer records across both systems, inconsistent formatting of names, cities, and country values, missing and invalid email addresses, and variations in phone number formats. Additionally, conflicting values were observed for key attributes such as annual spend and location data, highlighting the lack of standardization between systems.

WHAT WAS DONE:
A structured MDM pipeline was implemented, including data standardization (name casing, country normalization, phone formatting), entity resolution using email and name-phone matching, and survivorship rules to resolve attribute-level conflicts. System A was treated as the primary source for identity fields, while most recent values were used for location updates and highest values were used for financial fields. Unmatched records were retained as unique entities.

MASTER DATA SUMMARY:
The final master dataset contains a consolidated set of customer records derived from both systems. Source data included multiple duplicate and inconsistent records, which were successfully resolved into a unified golden record structure. The resulting master data provides a consistent, deduplicated, and validated view of customers, enabling improved reporting accuracy, governance, and business decision-making across all segments.
"""


# ----------------------------------------------------------------
# STEP 6 — Save the final MDM report
#
# TYPE code to write everything to mdm_report.txt
# Include the header, metrics, segment summary, and AI narrative.
# ----------------------------------------------------------------

report = f"""
================================================================
  MDM PROJECT REPORT — CUSTOMER MASTER DATA
  Prepared : {datetime.today().strftime('%B %d, %Y')}
================================================================

PROJECT METRICS
  Source records        : {total_source_records}
  Master records        : {total_master_records}
  Deduplication rate    : {dedup_rate:.1f}%
  Merged records        : {records_merged}
  System A only         : {records_a_only}
  System B only         : {records_b_only}

SEGMENT BREAKDOWN
{segment_summary.to_string(index=False)}

REPORT NARRATIVE
{ai_report.strip()}

================================================================
"""

# Save to file
with open('mdm_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)


print("mdm_report.txt saved!")
print()
print(report)

print("   You completed the full MDM workflow:")
print("   Task 1  Loaded two messy source systems")
print("   Task 2  Profiled and identified MDM problems")
print("   Task 3  Standardized both systems")
print("   Task 4  Matched and deduplicated records")
print("   Task 5  Applied survivorship rules and built golden records")
print("   Task 6  Validated the master data and built a lineage map")
print("   Task 7  Analyzed the results and produced an MDM report")
print()
print("   Deliverables: master_customers.csv, lineage_map.csv, mdm_report.txt")
