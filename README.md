# Business_Analytics

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
``` cd Aufgabe_Zwei\database ``` 
``` python ETL.py ```

### Backend starten:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **backend (FastAPI) starten**  im Business_Analytics Verzeichnis
``` uvicorn Aufgabe_Zwei.main:app --reload ```

### Frontend starten:
> **env Verzeichnis aktivieren**
``` env\Scripts\activate ```

> **frontend (streamlit) starten**
``` streamlit run Aufgabe_Zwei\frontend\frontend.py ```


