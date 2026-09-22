# InfluxDB-Lasttest und Monitoring mit Grafana

## Projektübersicht

Dieses Projekt wurde im Rahmen einer Modularbeit erstellt.

Ziel des Projekts ist es, eine InfluxDB-Instanz automatisiert bereitzustellen, einen kontrollierten Lasttest mit Python durchzuführen und die dabei entstehenden Messwerte anschliessend mit Grafana zu visualisieren.

Das Projekt besteht aus zwei Teilen:

### Modularbeit 1

- Bereitstellung von InfluxDB
- Durchführung eines Lasttests mit Python
- Messung von Requests, Fehlern und Antwortzeiten
- Speicherung der Ergebnisse in InfluxDB

### Modularbeit 2

- Bereitstellung von Grafana
- Automatische Konfiguration der InfluxDB-Datenquelle
- Automatische Bereitstellung eines Grafana-Dashboards
- Automatisierung der gesamten Umgebung mit Vagrant und Docker Compose

Die Umgebung kann mit Vagrant gestartet und anschliessend über Docker Compose innerhalb der virtuellen Maschine betrieben werden.

---

# Architektur

Die Umgebung besteht aus folgenden Komponenten:

```text
Host-System
    |
    | Vagrant
    v
Ubuntu VM
    |
    | Docker Compose
    |
    +---------------------+
    |                     |
    v                     v
InfluxDB               Grafana
Port 8086              Port 3000
    ^
    |
Python-Lasttest
```

Der Python-Lasttest sendet Abfragen an InfluxDB.

Nach Abschluss eines Lasttests werden die gemessenen Ergebnisse wieder in InfluxDB gespeichert.

Grafana verwendet InfluxDB als Datenquelle und visualisiert die gespeicherten Messwerte.

---

# Datenfluss

Der Datenfluss sieht folgendermassen aus:

```text
Python-Lasttest
      |
      | HTTP Requests
      v
   InfluxDB
      |
      | gespeicherte Lasttest-Messwerte
      v
    Grafana
      |
      v
   Dashboard
```

---

# Funktionsumfang

Das Projekt automatisiert folgende Aufgaben:

- Erstellung einer Ubuntu-VM mit Vagrant
- Unterstützung von VirtualBox und Parallels
- Installation von Docker
- Installation von Docker Compose
- Start von InfluxDB
- Start von Grafana
- Persistente Speicherung der Daten über Docker Volumes
- Automatische Konfiguration der InfluxDB-Datenquelle in Grafana
- Automatische Bereitstellung des Grafana-Dashboards
- Durchführung eines Python-basierten Lasttests
- Speicherung der Lasttest-Ergebnisse in InfluxDB
- Visualisierung der Ergebnisse in Grafana

---

# Verwendete Technologien

## Vagrant

Vagrant wird verwendet, um die virtuelle Maschine reproduzierbar zu erstellen und zu konfigurieren.

## Ubuntu

Die virtuelle Maschine verwendet Ubuntu als Betriebssystem.

## Docker

InfluxDB und Grafana werden als Docker-Container betrieben.

## Docker Compose

Docker Compose verwaltet die beiden Container und deren Konfiguration.

## InfluxDB

InfluxDB dient als Zeitreihendatenbank für die Messwerte des Lasttests.

## Grafana

Grafana visualisiert die in InfluxDB gespeicherten Messwerte.

## Python

Der Lasttest wurde mit Python entwickelt.

Für die HTTP-Kommunikation wird die Python-Bibliothek `requests` verwendet.

---

# Voraussetzungen

Auf dem Host-System werden folgende Programme benötigt:

- Vagrant
- VirtualBox oder Parallels
- Git

Bei der Verwendung von Parallels wird zusätzlich das entsprechende Vagrant-Parallels-Plugin benötigt.

---

# Projektstruktur

```text
Cybersecurity_Lastentest_Teko/
├── README.md
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── influx_loadtest.py
├── run-loadtest.sh
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── influxdb.yml
│   │   └── dashboards/
│   │       └── dashboards.yml
│   └── dashboards/
│       └── loadtest-dashboard.json
└── lastentest_vm/
    ├── Vagrantfile
    └── scripts/
        ├── system.sh
        ├── docker.sh
        ├── tools.sh
        └── stack.sh
```

---

# Umgebungsvariablen

Passwörter und Tokens werden nicht direkt in den Konfigurationsdateien gespeichert.

Dafür wird eine `.env`-Datei verwendet.

Beispiel:

```env
INFLUX_USERNAME=admin
INFLUX_PASSWORD=DEIN_PASSWORT
INFLUX_ORG=Iot
INFLUX_BUCKET=LoadTest
INFLUX_TOKEN='DEIN_INFLUX_TOKEN'

GRAFANA_USERNAME=admin
GRAFANA_PASSWORD=DEIN_PASSWORT
```

Die `.env`-Datei enthält sensible Informationen und darf nicht in das Git-Repository übertragen werden.

In `.gitignore` muss deshalb mindestens folgender Eintrag vorhanden sein:

```gitignore
.env
```

Optional kann eine `.env.example` ohne echte Zugangsdaten im Repository gespeichert werden.

---

# InfluxDB API Token

Der Python-Lasttest benötigt einen gültigen InfluxDB API Token.

Für dieses Projekt kann ein Custom API Token verwendet werden.

Der Token benötigt für den Bucket `LoadTest` folgende Berechtigungen:

```text
Read  → LoadTest
Write → LoadTest
```

Die Read-Berechtigung wird benötigt, da der Lasttest Abfragen gegen InfluxDB durchführt.

Die Write-Berechtigung wird benötigt, damit die Ergebnisse des Lasttests anschliessend in InfluxDB gespeichert werden können.

Der Token wird in der `.env`-Datei hinterlegt:

```env
INFLUX_TOKEN='DEIN_INFLUX_TOKEN'
```

Ein Custom Token mit ausschliesslichem Zugriff auf den benötigten Bucket folgt dem Prinzip der minimalen Berechtigungen.

---

# Umgebung starten

Zuerst in das Vagrant-Verzeichnis wechseln:

```bash
cd lastentest_vm
```

Anschliessend die virtuelle Maschine starten:

```bash
vagrant up
```

Vagrant erstellt die virtuelle Maschine und führt die Provisionierung aus.

Dabei werden unter anderem Docker und die benötigten Werkzeuge installiert.

---

# Provider auswählen

## VirtualBox

```bash
vagrant up --provider=virtualbox
```

## Parallels

```bash
vagrant up --provider=parallels
```

---

# Verbindung zur virtuellen Maschine

```bash
vagrant ssh
```

Danach in das Projektverzeichnis wechseln:

```bash
cd /project
```

---

# Docker-Container prüfen

Der Status der Container kann mit folgendem Befehl kontrolliert werden:

```bash
docker ps
```

Alternativ:

```bash
docker compose ps
```

Bei einer funktionierenden Umgebung sollten InfluxDB und Grafana als `healthy` angezeigt werden.

Beispiel:

```text
Grafana    Up (...) (healthy)
InfluxDB   Up (...) (healthy)
```

---

# InfluxDB prüfen

InfluxDB läuft auf Port `8086`.

Der Health-Endpunkt kann mit folgendem Befehl getestet werden:

```bash
curl http://localhost:8086/health
```

Eine funktionierende InfluxDB liefert einen Status wie:

```text
"status":"pass"
```

Die Weboberfläche ist über folgende Adresse erreichbar:

```text
http://localhost:8086
```

---

# Grafana prüfen

Grafana läuft auf Port `3000`.

Der Health-Endpunkt kann mit folgendem Befehl getestet werden:

```bash
curl http://localhost:3000/api/health
```

Die Weboberfläche ist über folgende Adresse erreichbar:

```text
http://localhost:3000
```

---

# Automatische InfluxDB-Konfiguration

InfluxDB wird beim ersten Start über Docker Compose konfiguriert.

Dabei werden unter anderem folgende Werte gesetzt:

```text
Organisation: Iot
Bucket:       LoadTest
```

Die Konfiguration wird über Umgebungsvariablen aus der `.env`-Datei gesteuert.

---

# Automatische Grafana-Konfiguration

Grafana wird über Provisioning-Dateien automatisch konfiguriert.

Die InfluxDB-Datenquelle befindet sich unter:

```text
grafana/provisioning/datasources/influxdb.yml
```

Innerhalb des Docker-Netzwerks verwendet Grafana folgende Adresse für InfluxDB:

```text
http://InfluxDB:8086
```

Grafana verwendet dabei die konfigurierte Organisation, den Bucket und einen gültigen InfluxDB-Token.

---

# Automatisches Grafana-Dashboard

Die Dashboard-Provisionierung befindet sich unter:

```text
grafana/provisioning/dashboards/dashboards.yml
```

Das eigentliche Dashboard befindet sich unter:

```text
grafana/dashboards/loadtest-dashboard.json
```

Das Dashboard visualisiert unter anderem:

- Anzahl Requests
- durchschnittliche Antwortzeit
- Anzahl Fehler
- P95-Antwortzeit

---

# Lasttest ausführen

Der Lasttest befindet sich in:

```text
influx_loadtest.py
```

Das Python-Skript unterstützt zwei Parameter:

```text
--requests
--workers
```

Mit `--requests` wird festgelegt, wie viele Requests insgesamt an InfluxDB gesendet werden.

Mit `--workers` wird festgelegt, wie viele Requests maximal parallel verarbeitet werden.

Eine feste Anzahl von Requests pro Sekunde oder eine feste Testdauer wird in der aktuellen Version nicht verwendet.

---

## Lasttest über das Startskript ausführen

Das Startskript befindet sich unter:

```text
run-loadtest.sh
```

Das Startskript lädt die benötigten Umgebungsvariablen aus der `.env`-Datei und startet anschliessend das Python-Skript.

Zuerst in das Projektverzeichnis wechseln:

```bash
cd /project
```

Falls nötig, das Startskript ausführbar machen:

```bash
chmod +x run-loadtest.sh
```

Kleiner Funktionstest:

```bash
./run-loadtest.sh --requests 10 --workers 2
```

Ein weiterer Test:

```bash
./run-loadtest.sh --requests 100 --workers 10
```

Ein mittlerer Lasttest:

```bash
./run-loadtest.sh --requests 1000 --workers 25
```

Ein grösserer Lasttest:

```bash
./run-loadtest.sh --requests 5000 --workers 50
```

Die Anzahl der Requests und Worker sollte kontrolliert und schrittweise erhöht werden.

---

# Erwartete Ausgabe des Lasttests

Bei einem erfolgreichen Test kann die Ausgabe beispielsweise so aussehen:

```text
URL:    http://localhost:8086
Org:    Iot
Bucket: LoadTest
Token:  gesetzt

Starte 10 Requests mit 2 Workern ...

Requests:      10
Erfolgreich:   10
Fehler:        0
Ø Antwortzeit: 12.20 ms
P95:           16.68 ms
```

Die konkreten Antwortzeiten unterscheiden sich je nach System und Auslastung.

---

# Funktionsweise des Lasttests

Das Python-Skript sendet parallele HTTP-Anfragen an die InfluxDB Query API.

Dabei wird unter anderem folgende Flux-Abfrage verwendet:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
  |> limit(n: 1000)
```

Die parallele Verarbeitung erfolgt über einen `ThreadPoolExecutor`.

Für jeden Request wird die Antwortzeit gemessen.

Nach Abschluss des Tests werden folgende Werte berechnet:

```text
requests
successes
errors
avg_latency_ms
p95_latency_ms
```

Diese Werte werden anschliessend als Measurement `loadtest` in InfluxDB gespeichert.

---

# Gespeicherte Messwerte

Das Measurement lautet:

```text
loadtest
```

Gespeichert werden folgende Felder:

```text
requests
successes
errors
avg_latency_ms
p95_latency_ms
```

Dabei bedeutet:

| Feld | Bedeutung |
|---|---|
| `requests` | Gesamtzahl der ausgeführten Requests |
| `successes` | Anzahl erfolgreicher Requests |
| `errors` | Anzahl fehlgeschlagener Requests |
| `avg_latency_ms` | durchschnittliche Antwortzeit in Millisekunden |
| `p95_latency_ms` | P95-Antwortzeit in Millisekunden |

---

# Daten in InfluxDB prüfen

Nach einem Lasttest können die gespeicherten Daten direkt im InfluxDB Data Explorer kontrolliert werden.

Alle Daten des Buckets der letzten Stunde:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
```

Nur die Lasttest-Messwerte:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "loadtest")
```

Nur die Anzahl Requests:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "requests")
```

Wenn hier Daten angezeigt werden, wurde das Ergebnis des Lasttests erfolgreich in InfluxDB gespeichert.

---

# Grafana Queries

## Requests

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "requests")
```

## Durchschnittliche Antwortzeit

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "avg_latency_ms")
```

## Fehler

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "errors")
```

## P95-Antwortzeit

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "p95_latency_ms")
```

---

# Interpretation der Ergebnisse

Die durchschnittliche Antwortzeit zeigt, wie schnell InfluxDB die Requests im Mittel verarbeitet.

Die P95-Antwortzeit zeigt, unter welcher Antwortzeit ungefähr 95 Prozent der gemessenen Requests liegen.

Die Anzahl Fehler zeigt, wie viele Requests nicht erfolgreich verarbeitet werden konnten.

Durch unterschiedliche Werte für `--requests` und `--workers` kann untersucht werden, wie sich eine höhere Parallelität auf die Antwortzeiten und die Fehlerquote auswirkt.

Beispielsweise können mehrere Tests mit gleicher Request-Anzahl und unterschiedlichen Worker-Zahlen durchgeführt werden:

```bash
./run-loadtest.sh --requests 1000 --workers 10
```

```bash
./run-loadtest.sh --requests 1000 --workers 25
```

```bash
./run-loadtest.sh --requests 1000 --workers 50
```

```bash
./run-loadtest.sh --requests 1000 --workers 100
```

Die Ergebnisse können anschliessend in Grafana miteinander verglichen werden.

---

# Testen der beiden Modularbeiten

## Modularbeit 1 – InfluxDB und Lasttest testen

Zuerst in das Vagrant-Verzeichnis wechseln:

```bash
cd lastentest_vm
```

VM starten:

```bash
vagrant up
```

Mit der VM verbinden:

```bash
vagrant ssh
```

In das Projekt wechseln:

```bash
cd /project
```

Container prüfen:

```bash
docker compose ps
```

InfluxDB prüfen:

```bash
curl http://localhost:8086/health
```

Lasttest starten:

```bash
./run-loadtest.sh --requests 100 --workers 10
```

Anschliessend können die Daten in InfluxDB im Bucket `LoadTest` kontrolliert werden.

Folgende Werte sollten vorhanden sein:

```text
requests
successes
errors
avg_latency_ms
p95_latency_ms
```

---

## Modularbeit 2 – Grafana und Automatisierung testen

Zuerst prüfen, ob die Container laufen:

```bash
cd /project
```

```bash
docker compose ps
```

Grafana-Provisionierung kontrollieren:

```bash
docker exec Grafana ls -la /etc/grafana/provisioning/datasources/
```

Dashboard-Dateien kontrollieren:

```bash
docker exec Grafana ls -la /var/lib/grafana/dashboards/
```

Danach Grafana im Browser öffnen:

```text
http://localhost:3000
```

Die InfluxDB-Datenquelle und das Dashboard sollten automatisch vorhanden sein.

Anschliessend einen neuen Lasttest durchführen:

```bash
./run-loadtest.sh --requests 1000 --workers 25
```

Danach das Grafana-Dashboard aktualisieren.

Der vollständige Datenfluss sollte nun funktionieren:

```text
Python → InfluxDB → Grafana → Dashboard
```

---

# Vollständige Automatisierung testen

Um zu überprüfen, ob die Umgebung reproduzierbar aufgebaut werden kann, kann die VM vollständig neu erstellt werden.

Achtung: Dabei können lokal gespeicherte Daten der VM gelöscht werden.

Im Vagrant-Verzeichnis:

```bash
vagrant destroy -f
```

Danach:

```bash
vagrant up
```

Mit der neuen VM verbinden:

```bash
vagrant ssh
```

Projekt öffnen:

```bash
cd /project
```

Container kontrollieren:

```bash
docker compose ps
```

Danach einen kleinen Lasttest durchführen:

```bash
./run-loadtest.sh --requests 100 --workers 10
```

---

# Erwartete Ergebnisse

| Test | Erwartetes Ergebnis |
|---|---|
| Vagrant startet | VM wird erfolgreich erstellt |
| Docker Compose startet | InfluxDB und Grafana laufen |
| InfluxDB Healthcheck | Status `pass` |
| Grafana Healthcheck | Datenbankstatus `ok` |
| Lasttest | Requests werden ausgeführt |
| Authentifizierung | Keine HTTP-401-Fehler |
| Speicherung | Measurement `loadtest` wird erstellt |
| InfluxDB | Lasttest-Messwerte sind sichtbar |
| Grafana Datasource | InfluxDB ist erreichbar |
| Grafana Dashboard | Messwerte werden dargestellt |

---

# Entwicklung von manuell zu automatisiert

Zu Beginn des Projekts wurden einzelne Komponenten manuell eingerichtet und getestet.

Im weiteren Verlauf wurde die Umgebung schrittweise automatisiert.

Die Automatisierung umfasst:

```text
Vagrant
   ↓
Ubuntu VM
   ↓
Docker Installation
   ↓
Docker Compose
   ↓
InfluxDB + Grafana
   ↓
Provisioning
   ↓
Python-Lasttest
```

Dadurch kann die Umgebung reproduzierbar aufgebaut werden.

---

# Bedienung und Fehlersuche

## Containerstatus prüfen

```bash
docker ps
```

oder:

```bash
docker compose ps
```

---

## InfluxDB Healthcheck

```bash
curl http://localhost:8086/health
```

---

## Grafana Healthcheck

```bash
curl http://localhost:3000/api/health
```

---

## InfluxDB-Organisation prüfen

Nach dem Laden der `.env`:

```bash
echo "$INFLUX_ORG"
```

Erwartet:

```text
Iot
```

---

## InfluxDB-Bucket prüfen

```bash
echo "$INFLUX_BUCKET"
```

Erwartet:

```text
LoadTest
```

---

## Prüfen, ob ein Token gesetzt ist

Der Token selbst sollte aus Sicherheitsgründen nicht im Terminal ausgegeben werden.

Stattdessen:

```bash
if [ -n "${INFLUX_TOKEN:-}" ]; then echo "Token vorhanden"; else echo "Token fehlt"; fi
```

---

## HTTP 401 Unauthorized

Wenn der Lasttest beispielsweise folgende Ausgabe liefert:

```text
HTTP 401: unauthorized access
```

ist die Authentifizierung gegenüber InfluxDB fehlgeschlagen.

Zuerst sollte geprüft werden, ob die `.env` geladen wurde:

```bash
cd /project
```

```bash
set -a
source .env
set +a
```

Danach kann der Lasttest erneut durchgeführt werden:

```bash
./run-loadtest.sh --requests 10 --workers 2
```

Falls weiterhin ein HTTP-401-Fehler auftritt, sollte kontrolliert werden, ob der in `.env` hinterlegte API Token noch gültig ist und die benötigten Berechtigungen besitzt.

Für den Lasttest benötigt der Custom API Token:

```text
Read  → LoadTest
Write → LoadTest
```

Ein Token sollte niemals in Dokumentationen, Screenshots oder öffentlichen Git-Repositories veröffentlicht werden.

---

# Grafana Provisioning prüfen

Datasource:

```bash
docker exec Grafana ls -la /etc/grafana/provisioning/datasources/
```

Dashboard:

```bash
docker exec Grafana ls -la /var/lib/grafana/dashboards/
```

Grafana-Logs:

```bash
docker logs Grafana 2>&1 | grep -i -E "influx|datasource|provision|error"
```

---

# Grafana zeigt keine Werte

Wenn das Dashboard vorhanden ist, aber keine Werte anzeigt, sollte zuerst geprüft werden, ob InfluxDB überhaupt Lasttest-Daten enthält.

Im InfluxDB Data Explorer:

```flux
from(bucket: "LoadTest")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "loadtest")
```

Wenn dort keine Ergebnisse erscheinen, liegt das Problem vor Grafana.

In diesem Fall sollte der Python-Lasttest kontrolliert werden.

Ein erfolgreicher Lasttest sollte beispielsweise folgende Werte zeigen:

```text
Erfolgreich: 10
Fehler:      0
```

Wenn InfluxDB Daten enthält, kann anschliessend die gleiche Flux-Abfrage in Grafana unter `Explore` getestet werden.

Wenn die Daten dort ebenfalls erscheinen, funktionieren InfluxDB und die Grafana-Datenquelle. In diesem Fall sollte die Query des jeweiligen Dashboard-Panels kontrolliert werden.

---

# Zeit und Zeitzone

Die virtuelle Maschine sollte die Zeitzone `Europe/Zurich` verwenden.

Die aktuelle Konfiguration kann geprüft werden:

```bash
timedatectl
```

Die Zeitzone kann gesetzt werden:

```bash
sudo timedatectl set-timezone Europe/Zurich
```

Die automatische Zeitsynchronisation kann aktiviert werden:

```bash
sudo timedatectl set-ntp true
```

Die aktuelle Zeit kann geprüft werden:

```bash
date
```

Auch die Container-Zeit kann kontrolliert werden.

InfluxDB:

```bash
docker exec InfluxDB date
```

Grafana:

```bash
docker exec Grafana date
```

Eine korrekte Systemzeit ist wichtig, da Grafana Messwerte anhand ihres Zeitstempels darstellt.

---

# Besonderheit bei Parallels

Bei Parallels wird das Projekt über `rsync` in die virtuelle Maschine übertragen.

Nach Änderungen auf dem Host-System kann eine erneute Synchronisierung notwendig sein.

Im Vagrant-Verzeichnis:

```bash
vagrant rsync
```

Danach befinden sich die synchronisierten Dateien unter:

```text
/project
```

Die Grafana-Verzeichnisse dürfen dabei nicht vom `rsync` ausgeschlossen werden, da sonst die Provisioning- und Dashboard-Dateien nicht in der VM verfügbar sind.

---

# Docker neu starten

Die Container können mit folgendem Befehl neu gestartet beziehungsweise neu erstellt werden:

```bash
docker compose up -d
```

Status prüfen:

```bash
docker compose ps
```

---

# Docker-Daten vollständig zurücksetzen

Falls die Umgebung vollständig zurückgesetzt werden soll:

```bash
docker compose down -v
```

Achtung:

Dieser Befehl löscht auch die Docker Volumes und damit gespeicherte InfluxDB- und Grafana-Daten.

Danach:

```bash
docker compose up -d
```

Dieser Schritt sollte nur durchgeführt werden, wenn ein vollständiger Reset gewünscht ist.

---

# VM neu erstellen

Die virtuelle Maschine kann vollständig entfernt werden:

```bash
vagrant destroy -f
```

Danach kann sie neu erstellt werden:

```bash
vagrant up
```

---

# Git und Sicherheit

Sensible Dateien dürfen nicht in das Repository übertragen werden.

Die `.gitignore` sollte mindestens folgende Einträge enthalten:

```gitignore
.env
venv/
.vagrant/
.DS_Store
*.box
```

Die `.env` enthält unter anderem:

- InfluxDB-Passwort
- InfluxDB API Token
- Grafana-Passwort

Diese Informationen dürfen nicht öffentlich veröffentlicht werden.

---

# Sicherheit des API Tokens

Für den Lasttest wird ein Custom API Token empfohlen.

Der Token erhält ausschliesslich die für den Lasttest benötigten Rechte:

```text
LoadTest → Read
LoadTest → Write
```

Dadurch erhält das Python-Skript keinen unnötigen administrativen Zugriff auf die gesamte InfluxDB-Instanz.

Falls ein Token versehentlich veröffentlicht wurde, sollte dieser in InfluxDB widerrufen und durch einen neuen Token ersetzt werden.

---

# Ausblick

Das Projekt kann in Zukunft erweitert werden.

Mögliche Erweiterungen sind:

- kontinuierliche Messwerte während eines laufenden Lasttests
- zusätzliche Laststufen
- automatische Vergleichstests
- CPU- und RAM-Monitoring
- Docker-Monitoring
- zusätzliche Grafana-Panels
- automatische Alarmierung bei hohen Antwortzeiten
- Export der Testergebnisse
- automatisierte Testberichte

---

# Sicherheitshinweis

Der Lasttest ist ausschliesslich für die eigene Labor- und Testumgebung vorgesehen.

Die Zieladresse des Lasttests lautet:

```text
http://localhost:8086
```

Dadurch wird ausschliesslich die lokal bereitgestellte InfluxDB-Instanz getestet.

Lasttests dürfen nicht ohne ausdrückliche Erlaubnis gegen fremde Systeme oder produktive Dienste durchgeführt werden.