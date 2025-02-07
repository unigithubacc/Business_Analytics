import sqlite3

# Connect to the first database (Personen)
conn1 = sqlite3.connect('personen.db')
cursor1 = conn1.cursor()

# Connect to the second database (Arbeitszeiten)
conn2 = sqlite3.connect('arbeitszeitenWeek.db')
cursor2 = conn2.cursor()

# Ensure the combined table exists in the second database
cursor2.execute('''
CREATE TABLE IF NOT EXISTS combined (
    ID INTEGER,
    Name TEXT,
    Abteilung TEXT,
    Standort TEXT,
    Position TEXT,
    Projekt TEXT,
    Week_1 REAL,
    Week_2 REAL,
    Week_3 REAL,
    Week_4 REAL,
    Week_5 REAL,
    Week_6 REAL,
    Week_7 REAL,
    Week_8 REAL,
    Week_9 REAL,
    Week_10 REAL,
    Week_11 REAL,
    Week_12 REAL,
    Week_13 REAL,
    Week_14 REAL,
    Week_15 REAL,
    Week_16 REAL,
    Week_17 REAL,
    Week_18 REAL,
    Week_19 REAL,
    Week_20 REAL,
    Week_21 REAL,
    Week_22 REAL,
    Week_23 REAL,
    Week_24 REAL,
    Week_25 REAL,
    Week_26 REAL,
    Week_27 REAL,
    Week_28 REAL,
    Week_29 REAL,
    Week_30 REAL,
    Week_31 REAL,
    Week_32 REAL,
    Week_33 REAL,
    Week_34 REAL,
    Week_35 REAL,
    Week_36 REAL,
    Week_37 REAL,
    Week_38 REAL,
    Week_39 REAL
)
''')
conn2.commit()

# Read data from the first database (Personen_Tabelle)
cursor1.execute("SELECT ID, Name, Abteilung, Standort, Position, Projekt FROM Personen_Tabelle")
personen_data = cursor1.fetchall()

# Read data from the second database (Arbeitszeiten_Tabelle)
cursor2.execute("SELECT ID, Name, Week_1, Week_2, Week_3, Week_4, Week_5, Week_6, Week_7, Week_8, Week_9, Week_10, Week_11, Week_12, Week_13, Week_14, Week_15, Week_16, Week_17, Week_18, Week_19, Week_20, Week_21, Week_22, Week_23, Week_24, Week_25, Week_26, Week_27, Week_28, Week_29, Week_30, Week_31, Week_32, Week_33, Week_34, Week_35, Week_36, Week_37, Week_38, Week_39 FROM Arbeitszeiten_Tabelle")
arbeitszeiten_data = cursor2.fetchall()

# Combine the data
combined_data = []
for person in personen_data:
    person_id = person[0]
    for arbeitszeit in arbeitszeiten_data:
        if arbeitszeit[0] == person_id:
            combined_row = (
                person_id,
                person[1],  # Name
                person[2],  # Abteilung
                person[3],  # Standort
                person[4],  # Position
                person[5],  # Projekt
                *arbeitszeit[2:]  # Week_1 to Week_39
            )
            combined_data.append(combined_row)

# Insert combined data into the new table
cursor2.executemany('''
INSERT INTO combined (
    ID, Name, Abteilung, Standort, Position, Projekt,
    Week_1, Week_2, Week_3, Week_4, Week_5, Week_6, Week_7, Week_8, Week_9, Week_10,
    Week_11, Week_12, Week_13, Week_14, Week_15, Week_16, Week_17, Week_18, Week_19, Week_20,
    Week_21, Week_22, Week_23, Week_24, Week_25, Week_26, Week_27, Week_28, Week_29, Week_30,
    Week_31, Week_32, Week_33, Week_34, Week_35, Week_36, Week_37, Week_38, Week_39
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', combined_data)

# Save changes and close connections
conn2.commit()
conn1.close()
conn2.close()

print("Daten wurden erfolgreich in die Tabelle 'combined' zusammengeführt.")