# InfluxDB-Lasttest und Monitoring mit Grafana

## Projektübersicht

Dieses Projekt wurde im Rahmen eines Security-Projekts erstellt.

Das Ziel besteht darin, eine reproduzierbare Testumgebung für InfluxDB aufzubauen, Lasttests automatisiert durchzuführen und die dabei entstehenden Messwerte mit Grafana zu visualisieren.

Das Projekt besteht aus zwei zentralen Teilen:

### Modularbeit 1 – InfluxDB und Lasttest

- Bereitstellung einer InfluxDB
- Entwicklung eines Python-Lasttests
- Parallele Requests gegen InfluxDB
- Messung der Antwortzeiten
- Erfassung erfolgreicher und fehlerhafter Requests
- Berechnung der durchschnittlichen Antwortzeit
- Berechnung der P95-Antwortzeit
- Speicherung der Testergebnisse in InfluxDB

### Modularbeit 2 – Grafana und Automatisierung

- Bereitstellung von Grafana
- Automatische Konfiguration der InfluxDB-Datenquelle
- Automatische Bereitstellung eines Grafana-Dashboards
- Visualisierung der Lasttest-Ergebnisse
- Automatisierter Aufbau der Umgebung mit Vagrant und Docker Compose

---

# Architektur

Die Testumgebung besteht aus mehreren Ebenen:

```text
Host-System
    |
    v
Vagrant
    |
    v
Ubuntu VM
    |
    v
Docker Compose
    |
    +-------------------+
    |                   |
    v                   v
InfluxDB              Grafana
Port 8086             Port 3000
    ^
    |
    |
Python-Lasttest
influx_loadtest.py
```

Vagrant stellt die virtuelle Maschine bereit.

Innerhalb der virtuellen Maschine werden InfluxDB und Grafana über Docker Compose gestartet.

Der Python-Lasttest erzeugt Requests gegen InfluxDB und speichert die Ergebnisse anschliessend wieder in InfluxDB.

Grafana liest diese Messwerte aus InfluxDB und stellt sie grafisch dar.

---

# Datenfluss

Der Datenfluss während eines Lasttests sieht folgendermassen aus:

```text
influx_loadtest.py
        |
        | Requests
        v
     InfluxDB
        |
        | Lasttest-Ergebnisse
        v
   Bucket LoadTest
        |
        | Flux Queries
        v
      Grafana
        |
        v
     Dashboard
```

Dadurch entsteht eine vollständige Kette von der Lastgenerierung bis zur Visualisierung.

---

# Funktionsumfang

Das Projekt bietet folgende Funktionen:

- Automatisierte Erstellung einer Ubuntu-VM
- Unterstützung von VirtualBox und Parallels
- Installation von Docker
- Start von InfluxDB über Docker Compose
- Start von Grafana über Docker Compose
- Persistente Speicherung der Daten
- Automatische Grafana-Provisionierung
- Automatische InfluxDB-Datenquelle in Grafana
- Automatisches Grafana-Dashboard
- Python-basierter Lasttest
- Konfigurierbare Anzahl von Requests
- Konfigurierbare Anzahl paralleler Worker
- Messung der Antwortzeiten
- Erfassung von Fehlern
- Berechnung des P95-Werts
- Speicherung der Lasttest-Ergebnisse in InfluxDB
- Visualisierung der Ergebnisse in Grafana

---

# Verwendete Technologien

Für das Projekt werden folgende Technologien verwendet:

```text
Vagrant
Ubuntu 24.04
Docker
Docker Compose
InfluxDB 2.7
Grafana
Python 3
Flux
Bash
Git
```

---

# Voraussetzungen

Auf dem Host-System werden benötigt:

- Vagrant
- VirtualBox oder Parallels
- Git

Für Parallels wird zusätzlich das entsprechende Vagrant-Parallels-Plugin benötigt.

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

Die Datei `influx_loadtest.py` enthält den eigentlichen Lasttest.

---

# Umgebungsvariablen

Zugangsdaten und Konfigurationswerte werden über eine `.env`-Datei verwaltet.

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

Die `.env`-Datei darf nicht in ein öffentliches Git-Repository übertragen werden.

Sie wird deshalb über `.gitignore` ausgeschlossen:

```gitignore
.env
venv/
.vagrant/
.DS_Store
*.box
```

Für das Repository kann stattdessen eine `.env.example` mit Platzhaltern verwendet werden.

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

Wenn ein neuer Token in InfluxDB erstellt wird, muss dieser ebenfalls in der `.env`-Datei aktualisiert werden.

Anschliessend müssen betroffene Container neu erstellt werden, damit der neue Token übernommen wird.

---

# Umgebung starten

Zuerst in das Verzeichnis mit dem Vagrantfile wechseln:

```bash
cd lastentest_vm
```

Danach die virtuelle Maschine starten:

```bash
vagrant up
```

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

Nach dem Start kann eine SSH-Verbindung zur VM hergestellt werden:

```bash
vagrant ssh
```

Das Projekt befindet sich innerhalb der VM unter:

```text
/project
```

In das Projektverzeichnis wechseln:

```bash
cd /project
```

---

# Zeitzone

Die virtuelle Maschine verwendet die Zeitzone `Europe/Zurich`.

Die Zeitzone kann mit folgendem Befehl gesetzt werden:

```bash
sudo timedatectl set-timezone Europe/Zurich
```

Die automatische Zeitsynchronisation kann aktiviert werden:

```bash
sudo timedatectl set-ntp true
```

Die aktuelle Konfiguration kann geprüft werden:

```bash
timedatectl
```

Die aktuelle Uhrzeit kann geprüft werden:

```bash
date
```

Die Docker-Container verwenden ebenfalls:

```yaml
TZ: Europe/Zurich
```

Dadurch verwenden VM und Container eine konsistente Zeitzone.

---

# Docker-Container prüfen

Innerhalb der VM:

```bash
cd /project
```

Danach:

```bash
sudo docker ps
```

Es sollten mindestens folgende Container laufen:

```text
InfluxDB
Grafana
```

Beide Container sollten nach erfolgreichem Start als `healthy` angezeigt werden.

---

# InfluxDB prüfen

InfluxDB ist über Port `8086` erreichbar.

Im Browser:

```text
http://localhost:8086
```

Der Zustand von InfluxDB kann innerhalb der VM zusätzlich geprüft werden:

```bash
curl http://localhost:8086/health
```

---

# Grafana prüfen

Grafana ist über Port `3000` erreichbar.

Im Browser:

```text
http://localhost:3000
```

Die Zugangsdaten werden über die `.env`-Datei definiert.

---

# Automatische InfluxDB-Konfiguration

InfluxDB wird beim ersten Start über Docker Compose initialisiert.

Dabei werden unter anderem folgende Werte verwendet:

```text
Organisation: Iot
Bucket:       LoadTest
```

Die Werte werden über die `.env`-Datei an Docker Compose übergeben.

---

# Automatische Grafana-Konfiguration

Grafana wird über Provisioning-Dateien automatisch konfiguriert.

Die InfluxDB-Datenquelle befindet sich unter:

```text
grafana/provisioning/datasources/influxdb.yml
```

Grafana verwendet innerhalb des Docker-Netzwerks folgende InfluxDB-Adresse:

```text
http://InfluxDB:8086
```

Innerhalb eines Docker-Containers darf hierfür nicht `localhost:8086` verwendet werden, da `localhost` auf den jeweiligen Container selbst zeigen würde.

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

Das Dashboard enthält folgende Messwerte:

```text
Requests
Durchschnittliche Antwortzeit
Fehler
P95-Antwortzeit
```

---

# Lasttest ausführen

Der Lasttest wird direkt über das Python-Skript ausgeführt:

```text
influx_loadtest.py
```

Das Skript unterstützt zwei zentrale Parameter:

```text
--requests
--workers
```

`--requests` definiert die Gesamtzahl der Requests.

`--workers` definiert die maximale Anzahl gleichzeitig ausgeführter Requests.

Eine feste Anzahl von Requests pro Sekunde oder eine feste Testdauer wird in der aktuellen Version nicht verwendet.

---

# Umgebungsvariablen vor dem Lasttest laden

Vor dem Start des Python-Skripts müssen die benötigten Umgebungsvariablen aus der `.env`-Datei geladen werden.

Zuerst:

```bash
cd /project
```

Danach:

```bash
set -a
source .env
set +a
```

Damit stehen unter anderem folgende Variablen für das Python-Skript zur Verfügung:

```text
INFLUX_ORG
INFLUX_BUCKET
INFLUX_TOKEN
```

---

# Leichter Lasttest

Für einen leichten Lasttest werden 100 Requests mit maximal 10 parallelen Workern ausgeführt:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Dieser Test eignet sich insbesondere zur Funktionskontrolle der Umgebung.

---

# Mittlerer Lasttest

Für einen mittleren Lasttest werden 1000 Requests mit maximal 25 parallelen Workern ausgeführt:

```bash
python3 influx_loadtest.py --requests 1000 --workers 25
```

Dieser Test erzeugt eine deutlich höhere Anzahl von Anfragen und eignet sich für einen Vergleich der Antwortzeiten.

---

# Schwerer Lasttest

Für einen schweren Lasttest werden 5000 Requests mit maximal 50 parallelen Workern ausgeführt:

```bash
python3 influx_loadtest.py --requests 5000 --workers 50
```

Die Last sollte kontrolliert und schrittweise erhöht werden.

---

# Übersicht der Laststufen

| Laststufe | Requests | Worker |
|---|---:|---:|
| Leicht | 100 | 10 |
| Mittel | 1000 | 25 |
| Schwer | 5000 | 50 |

Durch die verschiedenen Laststufen kann untersucht werden, wie sich eine höhere Anzahl von Requests und parallelen Workern auf die Antwortzeiten von InfluxDB auswirkt.

---

# Erwartete Ausgabe des Lasttests

Ein erfolgreicher Lasttest kann beispielsweise folgende Ausgabe erzeugen:

```text
URL:    http://localhost:8086
Org:    Iot
Bucket: LoadTest
Token:  gesetzt

Starte 100 Requests mit 10 Workern ...

Requests:      100
Erfolgreich:   100
Fehler:        0
Ø Antwortzeit: 12.20 ms
P95:           16.68 ms
```

Die tatsächlichen Antwortzeiten hängen von der verwendeten Hardware, der VM-Konfiguration und der aktuellen Systemlast ab.

---

# Funktionsweise des Lasttests

Der Python-Lasttest sendet parallele Anfragen an die InfluxDB.

Für die Parallelisierung werden mehrere Worker verwendet.

Der grundsätzliche Ablauf sieht folgendermassen aus:

```text
Python-Skript starten
        |
        v
Requests parallel ausführen
        |
        v
Antwortzeiten messen
        |
        v
Erfolge und Fehler zählen
        |
        v
Durchschnitt berechnen
        |
        v
P95 berechnen
        |
        v
Ergebnis in InfluxDB speichern
```

Dadurch kann untersucht werden, wie sich InfluxDB unter verschiedenen Laststufen verhält.

---

# Gespeicherte Messwerte

Nach Abschluss eines Lasttests werden die Ergebnisse in InfluxDB gespeichert.

Das verwendete Measurement lautet:

```text
loadtest
```

Dabei werden folgende Felder gespeichert:

```text
requests
successes
errors
avg_latency_ms
p95_latency_ms
```

## requests

Gesamtzahl der ausgeführten Requests.

## successes

Anzahl der erfolgreich ausgeführten Requests.

## errors

Anzahl der fehlgeschlagenen Requests.

## avg_latency_ms

Durchschnittliche Antwortzeit in Millisekunden.

## p95_latency_ms

P95-Antwortzeit in Millisekunden.

Der P95-Wert bedeutet, dass 95 Prozent der gemessenen Antwortzeiten kleiner oder gleich diesem Wert sind.

---

# Daten in InfluxDB prüfen

Nach einem Lasttest können die gespeicherten Ergebnisse direkt über den InfluxDB Data Explorer geprüft werden.

Beispiel:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "loadtest")
```

Nur die Anzahl der Requests kann beispielsweise folgendermassen abgefragt werden:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "requests")
```

---

# Grafana Queries

Grafana verwendet Flux Queries, um die gespeicherten Lasttest-Daten aus InfluxDB abzurufen.

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

Die wichtigsten Messwerte sind die durchschnittliche Antwortzeit und die P95-Antwortzeit.

Eine steigende durchschnittliche Antwortzeit bei höherer Last kann darauf hinweisen, dass InfluxDB stärker ausgelastet wird.

Der P95-Wert ist besonders hilfreich, weil einzelne langsame Requests dadurch besser sichtbar werden.

Zusätzlich sollte die Anzahl der Fehler betrachtet werden.

Wenn bei einer höheren Anzahl von Workern Fehler auftreten, kann dies auf eine Überlastung oder andere Einschränkungen der Testumgebung hinweisen.

Die Ergebnisse hängen stark von der verfügbaren CPU-Leistung, dem Arbeitsspeicher, der VM-Konfiguration und der Host-Hardware ab.

---

# Testen der beiden Modularbeiten

## Modularbeit 1 testen

Zuerst prüfen, ob InfluxDB läuft:

```bash
sudo docker ps
```

Danach die Umgebungsvariablen laden:

```bash
set -a
source .env
set +a
```

Anschliessend einen leichten Lasttest durchführen:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Wenn Requests erfolgreich verarbeitet und die Ergebnisse in InfluxDB gespeichert werden, funktioniert der erste Teil des Projekts.

---

## Modularbeit 2 testen

Prüfen, ob Grafana läuft:

```bash
sudo docker ps
```

Danach Grafana im Browser öffnen:

```text
http://localhost:3000
```

Das provisionierte Lasttest-Dashboard öffnen.

Die zuvor erzeugten Messwerte sollten dort dargestellt werden.

Damit wird geprüft, ob Grafana erfolgreich auf die Daten aus InfluxDB zugreifen kann.

---

# Vollständige Automatisierung testen

Um die gesamte Umgebung zu testen, kann die VM neu erstellt werden.

Zuerst:

```bash
cd lastentest_vm
```

Danach:

```bash
vagrant destroy -f
```

Anschliessend:

```bash
vagrant up
```

Danach:

```bash
vagrant ssh
```

In das Projektverzeichnis wechseln:

```bash
cd /project
```

Container prüfen:

```bash
sudo docker ps
```

Umgebungsvariablen laden:

```bash
set -a
source .env
set +a
```

Lasttest starten:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Anschliessend können die Ergebnisse über InfluxDB und Grafana kontrolliert werden.

---

# Erwartete Ergebnisse

| Test | Erwartetes Ergebnis |
|---|---|
| `vagrant up` | VM wird erfolgreich erstellt |
| `docker ps` | InfluxDB und Grafana laufen |
| InfluxDB Healthcheck | InfluxDB ist erreichbar |
| Python-Lasttest | Requests werden ausgeführt |
| InfluxDB Data Explorer | Lasttest-Daten sind vorhanden |
| Grafana-Datenquelle | Verbindung zu InfluxDB funktioniert |
| Grafana-Dashboard | Lasttest-Daten werden dargestellt |

---

# Entwicklung von manuell zu automatisiert

Während der Entwicklung wurden verschiedene Schritte zunächst manuell durchgeführt.

Dazu gehörten unter anderem:

- Starten der Container
- Konfiguration von InfluxDB
- Erstellen des API Tokens
- Konfiguration der Grafana-Datenquelle
- Erstellen der Grafana-Panels
- Ausführen des Python-Lasttests

Anschliessend wurden möglichst viele dieser Schritte automatisiert.

Dadurch kann die Testumgebung reproduzierbar aufgebaut werden.

---

# Bedienung und Fehlersuche

## `.env` wurde nicht geladen

Prüfen:

```bash
echo "$INFLUX_ORG"
```

```bash
echo "$INFLUX_BUCKET"
```

Der Token sollte aus Sicherheitsgründen nicht vollständig im Terminal ausgegeben werden.

Prüfen, ob ein Token gesetzt ist:

```bash
if [ -n "$INFLUX_TOKEN" ]; then echo "Token ist gesetzt"; else echo "Token fehlt"; fi
```

Falls die Variablen fehlen:

```bash
set -a
source .env
set +a
```

---

# HTTP 401 Unauthorized

Wenn der Python-Lasttest oder Grafana folgende Meldung liefert:

```text
HTTP 401
unauthorized access
```

sollte zuerst kontrolliert werden, ob der aktuelle API Token in `.env` eingetragen ist.

Der Custom API Token benötigt für dieses Projekt:

```text
Read  → LoadTest
Write → LoadTest
```

Wenn in InfluxDB ein neuer Token erstellt wurde, muss der Wert in `.env` aktualisiert werden.

Danach kann Grafana neu erstellt werden:

```bash
sudo docker compose up -d --force-recreate Grafana
```

Es sollte ebenfalls geprüft werden, ob Organisation und Bucket korrekt im Grafana-Container vorhanden sind:

```bash
sudo docker exec Grafana sh -c 'echo "ORG=$INFLUX_ORG | BUCKET=$INFLUX_BUCKET"'
```

Erwartet:

```text
ORG=Iot | BUCKET=LoadTest
```

Prüfen, ob der Token im Grafana-Container gesetzt wurde, ohne ihn anzuzeigen:

```bash
sudo docker exec Grafana sh -c 'echo "Token-Laenge: ${#INFLUX_TOKEN}"'
```

Ein eingeschränkter Custom API Token sollte nicht allgemein über `/api/v2/me` getestet werden.

Ein solcher Token kann bei diesem Endpunkt einen HTTP-401-Fehler liefern, wenn er keine Berechtigung zum Lesen von Benutzerdaten besitzt, obwohl die benötigten Lese- und Schreibzugriffe auf den Bucket funktionieren.

Deshalb sollte der Token über die tatsächlich benötigten Query- und Write-Funktionen getestet werden.

---

# Grafana Provisioning prüfen

Prüfen, ob die InfluxDB-Datenquelle im Container vorhanden ist:

```bash
sudo docker exec Grafana ls -la /etc/grafana/provisioning/datasources/
```

Datei anzeigen:

```bash
sudo docker exec Grafana cat /etc/grafana/provisioning/datasources/influxdb.yml
```

Umgebungsvariablen prüfen:

```bash
sudo docker exec Grafana env | grep INFLUX
```

Dabei ist zu beachten, dass dieser Befehl den Token anzeigen kann. Die Ausgabe sollte deshalb nicht veröffentlicht oder in Screenshots verwendet werden.

Grafana-Logs prüfen:

```bash
sudo docker logs Grafana 2>&1 | grep -i -E "datasource|provision|influx|unauthorized|error"
```

---

# Grafana zeigt keine Werte

Wenn das Dashboard keine Werte anzeigt, sollte zuerst geprüft werden, ob überhaupt Daten in InfluxDB vorhanden sind.

Im InfluxDB Data Explorer:

```flux
from(bucket: "LoadTest")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "loadtest")
```

Falls keine Daten vorhanden sind, einen neuen Lasttest durchführen:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Danach das Grafana-Dashboard aktualisieren.

Der Zeitraum in Grafana sollte beispielsweise auf folgendes eingestellt werden:

```text
Last 1 hour
```

oder:

```text
Last 24 hours
```

---

# Zeit und Zeitzone

Wenn Daten vorhanden sind, aber im Grafana-Zeitbereich nicht erscheinen, sollte die Uhrzeit geprüft werden.

```bash
date
```

```bash
timedatectl
```

Die Zeitzone kann auf Zürich gesetzt werden:

```bash
sudo timedatectl set-timezone Europe/Zurich
```

NTP aktivieren:

```bash
sudo timedatectl set-ntp true
```

Danach erneut prüfen:

```bash
timedatectl
```

---

# Besonderheit bei Parallels

Bei Parallels wird das Projekt über `rsync` in die VM übertragen.

Nach Änderungen auf dem Host kann deshalb eine erneute Synchronisation notwendig sein.

Im Verzeichnis `lastentest_vm`:

```bash
vagrant rsync
```

Danach kann innerhalb der VM geprüft werden, ob die Dateien vorhanden sind:

```bash
ls -la /project
```

Grafana-Dateien prüfen:

```bash
ls -la /project/grafana
```

Wichtig ist, dass der Ordner `grafana/` nicht von der rsync-Konfiguration ausgeschlossen wird.

---

# Docker neu starten

Alle Services können neu gestartet werden:

```bash
sudo docker compose restart
```

Oder neu erstellt werden:

```bash
sudo docker compose up -d --force-recreate
```

---

# Docker-Daten vollständig zurücksetzen

Falls ein vollständiger Reset notwendig ist:

```bash
sudo docker compose down -v
```

Danach:

```bash
sudo docker compose up -d
```

Achtung:

Der Parameter `-v` löscht die Docker-Volumes.

Dadurch können gespeicherte InfluxDB-Daten, Grafana-Daten und bestehende Konfigurationen verloren gehen.

Dieser Befehl sollte deshalb nur verwendet werden, wenn ein vollständiger Reset beabsichtigt ist.

---

# VM neu erstellen

Die virtuelle Maschine kann vollständig gelöscht werden:

```bash
vagrant destroy -f
```

Danach neu erstellen:

```bash
vagrant up
```

---

# Git und Sicherheit

Die `.env`-Datei darf nicht in Git eingecheckt werden.

Prüfen:

```bash
git status
```

Die `.gitignore` sollte mindestens enthalten:

```gitignore
.env
venv/
.vagrant/
.DS_Store
*.box
```

Insbesondere VM-Images und Vagrant-Pakete sollten nicht in das Repository aufgenommen werden, da diese sehr gross sein können.

---

# Sicherheit des API Tokens

API Tokens sollten wie Passwörter behandelt werden.

Folgende Regeln sollten beachtet werden:

- Token nicht direkt im Python-Code speichern
- Token nicht im README hinterlegen
- Token nicht in Screenshots veröffentlichen
- Token nicht in ein öffentliches Git-Repository übertragen
- `.env` über `.gitignore` ausschliessen
- Nur die tatsächlich benötigten Berechtigungen vergeben
- Nicht mehr benötigte Tokens in InfluxDB löschen oder widerrufen
- Bei einem versehentlich veröffentlichten Token einen neuen Token erstellen

Für dieses Projekt ist ein Custom Token mit Read- und Write-Zugriff auf den Bucket `LoadTest` ausreichend.

---

# Ausblick

Das Projekt kann zukünftig erweitert werden.

Mögliche Erweiterungen sind:

- Tests mit einer definierten Testdauer
- Begrenzung der Requests pro Sekunde
- Automatische Durchführung mehrerer Laststufen
- Vergleich mehrerer Testläufe
- Zusätzliche Grafana-Panels
- Überwachung von CPU- und RAM-Auslastung
- Export von Testergebnissen
- Automatische Erstellung eines Testberichts
- Alarmierung bei hohen Antwortzeiten oder Fehlerquoten
- Erweiterte Fehleranalyse

---

# Sicherheitshinweis

Die Testumgebung ist für Labor-, Lern- und Demonstrationszwecke vorgesehen.

Lasttests sollten ausschliesslich gegen Systeme durchgeführt werden, für die eine entsprechende Berechtigung vorliegt.

Die Last sollte schrittweise erhöht werden, damit die Auswirkungen auf das Zielsystem kontrolliert werden können.