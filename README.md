📊 Master Data Management (MDM) Project — Customer Data Consolidation
📌 Overview

This project demonstrates an end-to-end Master Data Management (MDM) pipeline built using Python. It simulates a real-world scenario where customer data from two different CRM systems is cleaned, standardized, matched, and consolidated into a single Golden Record (Customer 360 view).

The goal is to resolve duplicates, fix inconsistencies, and create a trusted master dataset for analytics and business decision-making.

🚀 Key Objectives
Identify and resolve duplicate customer records across systems
Standardize inconsistent data formats
Apply entity resolution (matching logic)
Define survivorship rules to resolve conflicts
Build a unified Golden Customer Master table
Ensure data quality and traceability (lineage)
🧱 Project Workflow
1. Data Ingestion
Loaded datasets from two CRM systems (System A & System B)
2. Data Profiling
Identified missing values, duplicates, and inconsistencies
3. Data Standardization
Fixed casing issues (names, cities)
Standardized country values
Normalized phone number formats
Validated email structure
4. Entity Matching
Matched customers using:
Exact email matching (high confidence)
Name + phone matching (secondary rule)
5. Survivorship Rules
System A → authoritative source for identity fields
Most recent value → location updates
Highest value → financial metrics (annual spend)
6. Golden Record Creation
Built unified customer records
Removed duplicates across systems
7. Data Validation & Lineage
Validated data quality rules
Built lineage map to track source systems
📊 Outputs
master_customers.csv → Final Golden Customer Table
lineage_map.csv → Data lineage tracking
mdm_report.txt → Full analytical report
Visualization: Customer segment spend analysis
🛠️ Tech Stack
Python (Pandas)
Data Cleaning & Transformation
Entity Resolution Logic
Basic Data Visualization (Matplotlib)
📈 Business Value

This project simulates a real telecom/enterprise MDM system and helps:

Improve customer data accuracy
Enable Customer 360 view
Reduce duplicates across systems
Support better analytics & decision-making
📚 Learning Outcome

This project demonstrates practical understanding of:

Master Data Management (MDM)
Data Quality Management
Entity Resolution
Survivorship Rules
Data Governance concepts
👩‍💻 Author

Dania Mohammed
