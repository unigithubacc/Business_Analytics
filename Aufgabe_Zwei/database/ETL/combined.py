import sqlite3

def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()

def create_combined_table(cursor):
    # Dynamische Erstellung der Wochen-Spalten
    weeks = [f"Week_{i} REAL" for i in range(1, 41)]
    columns = [
        "ID INTEGER",
        "Name TEXT",
        "Abteilung TEXT",
        "Standort TEXT",
        "Position TEXT",
        "Projekt TEXT",
        *weeks  # Fügt die Wochen-Spalten hinzu
    ]
    create_table_query = f"CREATE TABLE IF NOT EXISTS combined ({', '.join(columns)})"
    cursor.execute(create_table_query)

def fetch_data(cursor, table, columns):
    cursor.execute(f"SELECT {', '.join(columns)} FROM {table}")
    return cursor.fetchall()

def combine_data(personen_data, arbeitszeiten_data):
    combined_data = []
    for person in personen_data:
        person_id = person[0]
        for arbeitszeit in arbeitszeiten_data:
            if arbeitszeit[0] == person_id:
                combined_row = (*person, *arbeitszeit[2:])  # Kombiniert die Daten
                combined_data.append(combined_row)
    return combined_data

def insert_combined_data(cursor, data):
    # Dynamische Generierung der Spaltennamen und Platzhalter
    columns = [
        "ID", "Name", "Abteilung", "Standort", "Position", "Projekt",
        *[f"Week_{i}" for i in range(1, 41)]  # Spaltennamen für die Wochen
    ]
    placeholders = ", ".join(["?"] * len(columns))  # Platzhalter für die Werte
    insert_query = f"INSERT INTO combined ({', '.join(columns)}) VALUES ({placeholders})"
    cursor.executemany(insert_query, data)

def main():
    # Verbindung zu den Datenbanken herstellen
    conn1, cursor1 = connect_to_db('ETL/personen.db')
    conn2, cursor2 = connect_to_db('ETL/arbeitszeitenWeek.db')

    # Sicherstellen, dass die kombinierte Tabelle existiert
    create_combined_table(cursor2)
    conn2.commit()

    # Daten aus den Tabellen abrufen
    personen_data = fetch_data(cursor1, 'Personen_Tabelle', ['ID', 'Name', 'Abteilung', 'Standort', 'Position', 'Projekt'])
    arbeitszeiten_columns = ['ID', 'Name', *[f"Week_{i}" for i in range(1, 41)]]
    arbeitszeiten_data = fetch_data(cursor2, 'Arbeitszeiten_Tabelle', arbeitszeiten_columns)

    # Daten kombinieren
    combined_data = combine_data(personen_data, arbeitszeiten_data)

    # Kombinierte Daten in die neue Tabelle einfügen
    insert_combined_data(cursor2, combined_data)
    conn2.commit()

    # Verbindungen schließen
    conn1.close()
    conn2.close()

    print("Daten wurden erfolgreich in die Tabelle 'combined' zusammengeführt.")

if __name__ == "__main__":
    main()