import os
import sqlite3
import pandas as pd
from datetime import datetime

class Arbeitszeiten_ETL_Handler:
    """
    Klasse zum Einlesen einer CSV-Datei mit Arbeitszeiten und Speichern der Daten in einer SQLite-Datenbank.
    :param _csv_path: Pfad zur CSV-Datei
    :param _df: DataFrame mit den Daten aus der CSV-Datei
    """

    def __init__(
            self,
            _csv_path: str
    ):
        """
        Initialisiert die Klasse mit dem Pfad zur CSV-Datei. 

        :param _csv_path: Pfad zur CSV-Datei, welche die Arbeitszeiten enthält
        """
        self._csv_path = os.path.abspath(_csv_path)
        self.extract()

        # Bereinigung der Dezimalzahlen (Komma durch Punkt ersetzen)
        for column in self._df.columns[1:]:  # Spalte 0 ist der Name, daher beginnen wir mit der 1.
            self._df[column] = self._df[column].str.replace(',', '.').astype(float)

        self.transform()

    # extract ---------------------------------------------------------------------------------------------------------

    def extract(self) -> None:
        """
        Extrahiert die Daten aus der CSV-Datei und speichert sie in einem DataFrame.
        """
        self._df = pd.read_csv(
            self._csv_path,
            delimiter=';',  # Semikolon als Trennzeichen
        )

    # transform ---------------------------------------------------------------------------------------------------------

    def transform(self) -> None:
        """
        Transformiert die Arbeitszeitdaten und berechnet zusätzliche Werte.
        """
        # Kopiere den DataFrame, um Fragmentierung zu vermeiden
        self._df = self._df.copy()

        # Füge eine Spalte 'id' hinzu, die eine eindeutige ID für jede Zeile enthält
        self._df.insert(0, 'ID', range(1, 1 + len(self._df)))

        # Umwandeln der Spaltenüberschriften in Datumswerte
        date_columns = self._df.columns[2:]  # Spalten ab Index 2 sind Datumsangaben
        self._df.columns = ['ID', 'Name'] + [pd.to_datetime(col, format='%d.%m.%Y') for col in date_columns]

        # Umwandeln der Daten in ein langes Format (Melt)
        self._df_long = self._df.melt(id_vars=['ID', 'Name'], var_name='Datum', value_name='Arbeitszeit')

        # Sicherstellen, dass die Spalte 'Datum' den Datentyp datetime hat
        self._df_long['Datum'] = pd.to_datetime(self._df_long['Datum'])

        # Hinzufügen der Kalenderwoche (ISO-Woche)
        self._df_long['Week'] = self._df_long['Datum'].dt.isocalendar().week

        # Gruppieren nach ID, Name und Woche, und Summe der Arbeitszeiten berechnen
        self._df_sum = self._df_long.groupby(['ID', 'Name', 'Week'])['Arbeitszeit'].sum().unstack()

        # Umbenennen der Spalten in "Week_1", "Week_2", usw.
        self._df_sum.columns = [f'Week_{i}' for i in self._df_sum.columns]

        # Runden der Werte auf zwei Nachkommastellen
        self._df_sum = self._df_sum.round(2)

    # load ---------------------------------------------------------------------------------------------------------

    def save_to_db(
            self,
            db_name: str,
            table_name: str
    ) -> None:
        """
        Speichert die Daten in einer SQLite-Datenbank.

        :param db_name: Name der SQLite-Datenbank
        :param table_name: Name der Tabelle in der SQLite-Datenbank
        """
        with sqlite3.connect(db_name) as connection:
            self._df_sum.to_sql(
                table_name, connection, if_exists='replace', index=True)
            connection.commit()


class DB_Handler:
    def show_db(
            db_name: str,
            table_name: str
    ) -> None:
        """
        Liest die Daten aus der SQLite-Datenbank und gibt sie als Tabelle aus.

        :param db_name: Name der SQLite-Datenbank
        :param table_name: Name der Tabelle in der SQLite-Datenbank
        """
        with sqlite3.connect(db_name) as connection:
            query = f"SELECT * FROM {table_name} LIMIT 5"
            _df = pd.read_sql_query(query, connection)

        print(_df)


# Main ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Pfad zur Arbeitszeiten CSV-Datei
    CSV_PATH = r'..\Business_Analytics_Dateien\Arbeitszeiten.csv'

    # Initialisiere die Arbeitszeiten-Verarbeitungsklasse
    processor = Arbeitszeiten_ETL_Handler(CSV_PATH)

    # Pfad zur SQLite-Datenbank im gleichen Ordner wie das Skript
    DB_PATH = os.path.join(os.path.dirname(__file__), "arbeitszeitenWeek.db")
    TABLE_NAME = "Arbeitszeiten_Tabelle"

    # Speichert die Daten in der SQLite-Datenbank
    processor.save_to_db(DB_PATH, TABLE_NAME)

    # Zeigt die gespeicherten Daten aus der SQLite-Datenbank an
    DB_Handler.show_db(DB_PATH, TABLE_NAME)