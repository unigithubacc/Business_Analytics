import pandas as pd

# Laden der CSV-Datei mit Semikolon als Trennzeichen
df = pd.read_csv(r'Business_Analytics_Dateien\Arbeitszeiten.csv', delimiter=';')

# Bereinigung der Dezimalzahlen (Komma durch Punkt ersetzen)
for column in df.columns[1:]:  # Spalte 0 ist der Name, daher beginnen wir mit der 1.
    df[column] = df[column].str.replace(',', '.').astype(float)

# Umwandeln der Datumsformat-Spalten in Wochentage (nur ab der zweiten Spalte)
df.columns = ['Name'] + [pd.to_datetime(col, format='%d.%m.%Y').strftime('%A') for col in df.columns[1:]]

# Setzen des Index auf den Namen des Mitarbeiters
df = df.set_index('Name')

# Umwandeln der Daten in ein langes Format (Melt)
df_long = df.reset_index().melt(id_vars=['Name'], var_name='Wochentag', value_name='Arbeitszeit')

# Ausgabe der bereinigten Daten (Arbeitszeit pro Mitarbeiter und Wochentag)
print("Arbeitszeit pro Mitarbeiter und Wochentag:")
print(df_long)

# Berechnung der Arbeitszeit pro Mitarbeiter*in pro Woche
df_long['Woche'] = df_long.groupby('Name')['Arbeitszeit'].transform('sum')

# Anzeige der Daten mit Arbeitszeit pro Woche
df_weekly = df_long[['Name', 'Woche']].drop_duplicates()

# Ausgabe der Daten zur Arbeitszeit pro Woche
print("\nArbeitszeit pro Woche pro Mitarbeiter:")
print(df_weekly)
