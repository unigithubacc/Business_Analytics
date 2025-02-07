import sqlite3

# Connect to the first database
conn1 = sqlite3.connect('personen.db')
cursor1 = conn1.cursor()

# Connect to the second database
conn2 = sqlite3.connect('arbeitszeitenWeek.db')
cursor2 = conn2.cursor()

# Ensure the table exists in the second database with the same structure
cursor2.execute('''
CREATE TABLE IF NOT EXISTS Personen_Tabelle (
    personID INTEGER,
    ID INTEGER,
    Name TEXT,
    Abteilung TEXT,
    Standort TEXT,
    Position TEXT,
    Projekt TEXT
)
''')
conn2.commit()

# Read data from the first database
cursor1.execute("SELECT personID, ID, Name, Abteilung, Standort, Position, Projekt FROM Personen_Tabelle")
rows = cursor1.fetchall()

# Insert data into the second database
cursor2.executemany('''
INSERT INTO Personen_Tabelle (personID, ID, Name, Abteilung, Standort, Position, Projekt)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', rows)

# Save changes and close connections
conn2.commit()
conn1.close()
conn2.close()

print("Daten wurden erfolgreich zusammengeführt.")
