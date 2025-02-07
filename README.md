# Business_Analytics

cd Aufgabe_Zwei\database 

## Installation und Start
### Projekt installation:
> **Virtuale Umgebung erzeugen**
``` python -m venv env ```

> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **Requirements installieren**
``` pip install -r requirements.txt ```

### Datenbank aufbauen:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **ETL ausführen**
``` python python weeks.py ```
``` python days.py ```
``` python person.py ```
``` python combined.py```


### Backend starten:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **backend (FastAPI) starten** 
``` uvicorn Aufgabe_Zwei.main:app --reload ```

### Frontend starten:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **frontend (streamlit) starten**
``` streamlit frontend.py ```


