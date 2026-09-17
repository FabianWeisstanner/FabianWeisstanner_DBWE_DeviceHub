# DeviceHub

DeviceHub ist eine webbasierte IT-Geräteverwaltung, die im Rahmen der Praxisarbeit  
**DBWE.TA1A.PA – IT-Architektur, Datenbank und Web-Entwicklung** entwickelt wurde.

Die Anwendung ermöglicht die Verwaltung von IT-Geräten über eine interaktive Weboberfläche und stellt zusätzlich eine authentisierte REST-API zur Verfügung.

---

## Funktionen

DeviceHub bietet folgende Funktionen:

- Benutzerregistrierung mit eindeutigem Benutzernamen und E-Mail-Adresse
- Login und Logout über Benutzerkonten
- Sichere Speicherung von Passwörtern als Hash
- Erfassen von IT-Geräten
- Bearbeiten bestehender Geräte
- Löschen von Geräten
- Verhindern doppelter Seriennummern
- Suche nach Geräten
- Filterung nach Status und Betriebssystem
- Dashboard mit Übersicht über den Gerätebestand
- REST-API für den lesenden Zugriff auf Gerätedaten
- Token-basierte Authentisierung der REST-API
- CSRF-Schutz für Webformulare

---

## Verwendete Technologien

| Bereich | Technologie |
|---|---|
| Programmiersprache | Python 3.11 |
| Web-Framework | Flask |
| Datenbank | PostgreSQL |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Benutzerverwaltung | Flask-Login |
| Formularschutz | Flask-WTF / CSRF |
| Webserver | Gunicorn |
| Frontend | HTML, Jinja2, Bootstrap 5 |
| Deployment | Replit Autoscale |
| Versionsverwaltung | Git / GitHub |

---

## Architektur

Die Anwendung basiert auf einer mehrschichtigen Architektur:

```text
Benutzer / API-Client
        |
        v
Weboberfläche / REST-API
        |
        v
Flask-Anwendung
        |
        v
SQLAlchemy
        |
        v
PostgreSQL
```

Die Anwendung verwendet zwei zentrale Datenobjekte:

- `User`
- `Device`

Ein Benutzer kann mehrere Geräte erfassen.  
Die Beziehung zwischen Benutzer und Gerät wird über das Feld `created_by` hergestellt.

---

## Projektstruktur

```text
DeviceHub/
├── app.py
├── models.py
├── extensions.py
├── requirements.txt
├── README.md
├── .gitignore
├── .replit
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── devices.html
│   ├── device_add.html
│   └── device_edit.html
└── artifacts/
    └── devicehub/
```

### Wichtige Dateien

#### `app.py`

Enthält die Flask-Anwendung, Webrouten, Authentisierung, Geschäftslogik, Geräteverwaltung und REST-API.

#### `models.py`

Enthält die SQLAlchemy-Datenmodelle `User` und `Device`.

#### `extensions.py`

Initialisiert die gemeinsam verwendete SQLAlchemy-Erweiterung.

#### `templates/`

Enthält die Jinja2-HTML-Templates für die Weboberfläche.

#### `requirements.txt`

Enthält die benötigten Python-Abhängigkeiten.

---

## Datenmodell

### User

Ein Benutzer besitzt folgende zentrale Attribute:

- ID
- Benutzername
- E-Mail-Adresse
- Passwort-Hash
- Erstellungsdatum

Benutzername und E-Mail-Adresse müssen eindeutig sein.

### Device

Ein Gerät enthält unter anderem:

- ID
- Gerätename
- Hersteller
- Modell
- Seriennummer
- Betriebssystem
- Gerätetyp
- Besitzer
- Status
- Erstellungsdatum
- Ersteller

Die Seriennummer eines Gerätes muss eindeutig sein.

Unterstützte Gerätestatus:

- `Active`
- `In Stock`
- `Repair`
- `Retired`

---

## REST-API

Neben der interaktiven Weboberfläche stellt DeviceHub eine REST-API für den lesenden Zugriff auf Gerätedaten bereit.

Die API verwendet eine Bearer-Token-Authentisierung.

---

### API-Token anfordern

```http
POST /api/auth/token
```

Beispiel:

```bash
curl -X POST \
  https://<DEVICEHUB-URL>/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"<USERNAME>","password":"<PASSWORD>"}'
```

Beispiel einer erfolgreichen Antwort:

```json
{
  "expires_in": 3600,
  "token": "<TOKEN>",
  "token_type": "Bearer"
}
```

Der Token ist für 3600 Sekunden gültig.

---

### Alle Geräte abrufen

```http
GET /api/devices
```

Beispiel:

```bash
curl \
  https://device-hub-fabianweisstanner.replit.app/api/devices \
  -H "Authorization: Bearer <TOKEN>"
```

Ohne gültige Authentisierung antwortet die API mit:

```text
HTTP 401 Unauthorized
```

---

### Einzelnes Gerät abrufen

```http
GET /api/devices/<id>
```

Beispiel:

```bash
curl \
  https://device-hub-fabianweisstanner.replit.app/api/devices/1 \
  -H "Authorization: Bearer <TOKEN>"
```

Die Antwort erfolgt im JSON-Format.

Beispiel:

```json
{
  "id": 1,
  "device_name": "Testdevice",
  "manufacturer": "HP",
  "model": "Surface",
  "serial_number": "Test-SN",
  "operating_system": "Windows 11",
  "device_type": "Surface",
  "owner": "Testuser",
  "status": "Active",
  "created_by": 1
}
```

---

## Installation

Benötigt wird Python 3.9 oder neuer.

Repository klonen:

```bash
git clone https://github.com/FabianWeisstanner/FabianWeisstanner_DBWE_DeeviceHub.git
```

In das Projektverzeichnis wechseln:

```bash
cd FabianWeisstanner_DBWE_DeeviceHub
```

Python-Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

---

## Umgebungsvariablen

Für den Betrieb der Anwendung werden folgende Umgebungsvariablen benötigt:

```text
DATABASE_URL
SECRET_KEY
```

### DATABASE_URL

Enthält die Verbindungszeichenfolge zur PostgreSQL-Datenbank.

### SECRET_KEY

Wird von Flask für Sessions und Sicherheitsfunktionen verwendet.

Sensible Werte werden nicht direkt im Source Code oder im Repository gespeichert.

---

## Lokaler Start

Für Entwicklungszwecke kann die Anwendung direkt über Python gestartet werden:

```bash
python app.py
```

Für den Betrieb über Gunicorn:

```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

---

## Deployment

DeviceHub wird über Replit bereitgestellt.

Die produktive Anwendung verwendet:

- Replit Autoscale
- Gunicorn als Webserver
- PostgreSQL als relationale Datenbank
- HTTPS für den öffentlichen Zugriff

### Webanwendung

```text
URL:
https://device-hub-fabianweisstanner.replit.app/
```

Die Benutzerregistrierung ist direkt über die Weboberfläche möglich.

---

## Sicherheit

Folgende Sicherheitsmassnahmen wurden umgesetzt:

- Passwörter werden nicht im Klartext gespeichert
- Passwort-Hashing über Werkzeug
- Session-basierte Authentisierung für die Weboberfläche
- Bearer-Token-Authentisierung für die REST-API
- CSRF-Schutz für POST-Formulare
- Eindeutige Benutzernamen
- Eindeutige E-Mail-Adressen
- Eindeutige Seriennummern für Geräte
- Verwendung eines `SECRET_KEY`
- Datenbankzugangsdaten werden als Umgebungsvariablen gespeichert
- Sensible Daten werden nicht im GitHub-Repository abgelegt

---

## Geschäftslogik

DeviceHub enthält eigene Geschäftslogik zur Validierung und Verarbeitung von Daten.

Dazu gehören unter anderem:

- Prüfung auf vollständig ausgefüllte Pflichtfelder
- Prüfung auf eindeutige Benutzernamen
- Prüfung auf eindeutige E-Mail-Adressen
- Prüfung auf eindeutige Seriennummern
- Verwaltung definierter Gerätestatus
- Suche nach Geräten
- Filterung nach Status
- Filterung nach Betriebssystem
- Berechnung der Geräteanzahl für das Dashboard

---

## Dashboard

Das Dashboard zeigt eine Übersicht über den aktuellen Gerätebestand.

Folgende Werte werden dargestellt:

- Gesamtanzahl Geräte
- Active
- In Stock
- Repair
- Retired

---

## Tests

Die wichtigsten funktionalen Anforderungen wurden manuell getestet.

| ID | Testfall | Erwartetes Ergebnis |
|---|---|---|
| T01 | Benutzer erfolgreich registrieren | Benutzer wird in der Datenbank gespeichert |
| T02 | Doppelten Benutzernamen verwenden | Registrierung wird verhindert |
| T03 | Anmeldung mit gültigen Zugangsdaten | Benutzer wird angemeldet |
| T04 | Anmeldung mit falschem Passwort | Anmeldung wird abgewiesen |
| T05 | Neues Gerät erfassen | Gerät wird gespeichert und angezeigt |
| T06 | Doppelte Seriennummer verwenden | Speicherung wird verhindert |
| T07 | Gerät bearbeiten | Änderungen werden gespeichert |
| T08 | Gerät löschen | Gerät wird aus der Datenbank entfernt |
| T09 | API ohne Token aufrufen | HTTP 401 Unauthorized |
| T10 | API mit gültigem Token aufrufen | HTTP 200 und JSON-Antwort |

Das vollständige Testprotokoll mit den tatsächlichen Testergebnissen ist Bestandteil der schriftlichen Praxisarbeit.

---

## Repository

Der vollständige Source Code der Anwendung wird über dieses GitHub-Repository bereitgestellt:

```text
https://github.com/FabianWeisstanner/FabianWeisstanner_DBWE_DeeviceHub
```

Das Repository enthält den Python-Quellcode, die HTML-Templates, die Abhängigkeiten und die für den Betrieb benötigten Konfigurationsdateien.

Sensible Informationen wie Datenbankpasswörter oder Secret Keys sind nicht Bestandteil des Repositorys.

---

## Hinweise zur Abgabe

Der Source Code wird zusätzlich zur Bereitstellung auf GitHub als ZIP-Datei zusammen mit der schriftlichen Praxisarbeit eingereicht.

Die veröffentlichte Webanwendung bleibt während der vorgesehenen Korrekturzeit verfügbar.

---

## Autor

**Fabian Weisstanner**

Praxisarbeit  
**DBWE.TA1A.PA – IT-Architektur, Datenbank und Web-Entwicklung**

Dipl. Informatiker HF Plattformentwicklung
