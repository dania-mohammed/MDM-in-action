import pandas as pd

# ── System A records (original CRM) ─────────────────────────
system_a = pd.DataFrame({
    'source':        ['A'] * 15,
    'source_id':     ['A001','A002','A003','A004','A005',
                      'A006','A007','A008','A009','A010',
                      'A011','A012','A013','A014','A015'],
    'first_name':    ['Alice','Bob','carol','DAVID','Eve',
                      'Frank','Grace','henry','Iris','Jack',
                      'Karen','Leo','Mia','Noah','Olivia'],
    'last_name':     ['Johnson','Smith','White','Brown','Davis',
                      'Miller','Wilson','Moore','Taylor','Anderson',
                      'Thomas','Jackson','Harris','Martin','Lee'],
    'email':         ['alice.johnson@email.com','bob.smith@email.com',
                      'carol.white@email.com','david.brown@email.com',
                      'eve.davis@email.com','frank.miller@',
                      'grace.wilson@email.com','henry.moore@email.com',
                      'iris.taylor@email.com','jack.anderson@email.com',
                      'karen.thomas@email.com','leo.jackson@email.com',
                      'mia.harris@email.com','','olivia.lee@email.com'],
    'phone':         ['555-0101','555-0102','5550103','555-0104','555-0105',
                      '555-0106','555-0107','555-0108','555-0109','555-0110',
                      '555-0111','555-0112','555-0113','555-0114','555-0115'],
    'city':          ['New York','Los Angeles','Chicago','Houston','Phoenix',
                      'Philadelphia','San Antonio','San Diego','Dallas','San Jose',
                      'Austin','Jacksonville','Fort Worth','Columbus','Charlotte'],
    'country':       ['USA','USA','USA','USA','USA',
                      'USA','USA','USA','USA','USA',
                      'USA','USA','USA','USA','USA'],
    'segment':       ['Enterprise','SMB','SMB','Enterprise','Startup',
                      'SMB','Enterprise','Startup','SMB','Enterprise',
                      'Startup','SMB','Enterprise','SMB','Startup'],
    'annual_spend':  [45000,12000,8500,67000,3200,
                      15000,52000,2800,9100,78000,
                      4100,11000,61000,7300,5600],
    'last_updated':  ['2024-01-15','2024-02-20','2024-01-08','2024-03-12','2024-02-05',
                      '2024-01-22','2024-03-18','2024-02-14','2024-01-30','2024-03-25',
                      '2024-02-08','2024-01-12','2024-03-05','2024-02-28','2024-01-19']
})

# ── System B records (acquired company CRM) ─────────────────
system_b = pd.DataFrame({
    'source':        ['B'] * 15,
    'source_id':     ['B001','B002','B003','B004','B005',
                      'B006','B007','B008','B009','B010',
                      'B011','B012','B013','B014','B015'],
    'first_name':    ['Alice','BOB','Paula','David','Eve',
                      'Frank','Quinn','Henry','Rachel','Jack',
                      'karen','Sam','Mia','Tina','Olivia'],
    'last_name':     ['Johnson','Smith','Adams','Brown','Davis',
                      'Miller','Green','Moore','Clark','Anderson',
                      'Thomas','Baker','Harris','Scott','Lee'],
    'email':         ['alice.johnson@email.com','b.smith@email.com',
                      'paula.adams@email.com','d.brown@email.com',
                      'eve.davis@email.com','frank.miller@email.com',
                      'quinn.green@email.com','henry.moore@email.com',
                      'rachel.clark@email.com','jack.anderson@email.com',
                      'karen.thomas@email.com','sam.baker@email.com',
                      'mia.harris@email.com','tina.scott@email.com',''],
    'phone':         ['555-0101','555-0102','555-0201','555-0104','555-0105',
                      '555-0106','555-0207','555-0108','555-0209','555-0110',
                      '555-0111','555-0212','555-0113','555-0214','555-0115'],
    'city':          ['New York','Los Angeles','Miami','houston','Phoenix',
                      'Philadelphia','Denver','San Diego','Seattle','San Jose',
                      'Austin','Portland','Fort Worth','Nashville','Charlotte'],
    'country':       ['US','USA','USA','USA','USA',
                      'USA','USA','usa','USA','USA',
                      'USA','USA','USA','USA','USA'],
    'segment':       ['Enterprise','SMB','Startup','Enterprise','Startup',
                      'SMB','Startup','Startup','SMB','Enterprise',
                      'Startup','SMB','Enterprise','SMB','Startup'],
    'annual_spend':  [47000,12500,4100,66000,3200,
                      15500,2100,2800,6700,78500,
                      4100,8900,61000,5200,5600],
    'last_updated':  ['2024-03-20','2024-01-15','2024-02-10','2024-03-28','2024-02-05',
                      '2024-03-01','2024-01-18','2024-02-22','2024-03-10','2024-02-28',
                      '2024-03-15','2024-01-25','2024-02-18','2024-03-22','2024-03-08']
})

# ── Combine both sources ─────────────────────────────────────
df = pd.concat([system_a, system_b], ignore_index=True)

# ── Save it ──────────────────────────────────────────────────
system_a.to_csv('system_a.csv', index=False)
system_b.to_csv('system_b.csv', index=False)
df.to_csv('customers_raw.csv', index=False)

# ── Preview ──────────────────────────────────────────────────
print(" Dataset ready!\n")
print(f"System A records : {len(system_a)}")
print(f"System B records : {len(system_b)}")
print(f"Combined records : {len(df)}")
print()
print("SYSTEM A (first 5 rows):")
print(system_a.head().to_string(index=False))
print()
print("SYSTEM B (first 5 rows):")
print(system_b.head().to_string(index=False))
print()
print(" This dataset contains duplicates, conflicts, and")
print("   inconsistencies across both systems.")
print("   Your job is to resolve them and produce one clean")
print("   master record per customer.")


