# InfluxDB-Lasttest und Monitoring mit Grafana

## Projektübersicht

Dieses Projekt stellt eine automatisierte Laborumgebung für die Durchführung und Auswertung von Lasttests auf einer InfluxDB bereit. Ein Python-Skript erzeugt eine kontrollierte Anzahl paralleler Abfragen gegen InfluxDB und misst dabei unter anderem die Antwortzeiten und aufgetretenen Fehler. Die Ergebnisse werden wieder in InfluxDB gespeichert und anschliessend mit Grafana visualisiert.

Die Umgebung wurde zunächst manuell aufgebaut und getestet. Dabei wurden InfluxDB und Grafana einzeln installiert und konfiguriert. Nachdem die grundlegende Funktion sichergestellt war, wurde die Umgebung mit Docker Compose automatisiert.

Vagrant stellt eine Ubuntu-VM bereit und installiert die benötigten Voraussetzungen. Docker Compose startet und konfiguriert InfluxDB und Grafana. Die Grafana-Datenquelle sowie das Dashboard werden über Provisioning automatisch eingerichtet.

Dadurch kann die vollständige Testumgebung nach dem Klonen des Projekts weitgehend automatisiert mit Vagrant aufgebaut werden.

Die Dokumentation gliedert das Projekt in zwei aufeinander aufbauende Modularbeiten:

- **Modularbeit 1 – InfluxDB und Lasttest:** Installation und Konfiguration von InfluxDB sowie Entwicklung eines Python-Skripts zur Durchführung eines Lasttests.
- **Modularbeit 2 – Grafana und Automatisierung:** Visualisierung der Lasttest-Ergebnisse mit Grafana und anschliessende Automatisierung der gesamten Umgebung mit Docker Compose und Vagrant.

> Die Umgebung ist ausschliesslich für Schulungs- und Testzwecke vorgesehen. Der Lasttest darf nur gegen die eigene Laborumgebung oder gegen Systeme durchgeführt werden, für die eine ausdrückliche Genehmigung vorliegt.

---

# Abgrenzung der beiden Modularbeiten

## Modularbeit 1 – InfluxDB und Lasttest

Ziel der ersten Modularbeit ist der Aufbau einer InfluxDB und die Entwicklung eines kontrollierten Lasttests.

InfluxDB wurde zunächst manuell auf einer Ubuntu-VM installiert und konfiguriert. Dabei wurden die benötigte Organisation, der Bucket und ein API-Token eingerichtet.

Für die Durchführung des Lasttests wurde ein Python-Skript entwickelt. Das Skript sendet mehrere parallele Flux-Abfragen an InfluxDB und misst die Antwortzeiten der einzelnen Requests.

Für die Auswertung werden unter anderem folgende Werte erfasst:

- Anzahl der Requests
- erfolgreiche Requests
- fehlerhafte Requests
- durchschnittliche Antwortzeit
- P95-Antwortzeit

Die Ergebnisse werden anschliessend wieder in den InfluxDB-Bucket `LoadTest` geschrieben.

Dadurch können sowohl die Belastung der Datenbank als auch die Auswirkungen einer steigenden Anzahl paralleler Anfragen untersucht werden.

## Modularbeit 2 – Grafana und Automatisierung

Die zweite Modularbeit erweitert die bestehende Umgebung um Grafana.

Grafana wurde zunächst manuell installiert und mit InfluxDB verbunden. Anschliessend wurden Flux-Abfragen erstellt, mit denen die Ergebnisse des Lasttests grafisch dargestellt werden können.

Das Dashboard visualisiert folgende Messwerte:

- Requests
- durchschnittliche Antwortzeit
- Fehler
- P95-Antwortzeit

Nachdem die manuelle Installation und Konfiguration erfolgreich getestet wurde, wurde die Umgebung automatisiert.

InfluxDB und Grafana werden nun als Docker-Container betrieben. Docker Compose übernimmt den Start und die Konfiguration der Dienste.

Grafana wird über Provisioning automatisch konfiguriert. Dadurch werden beim Start:

- die InfluxDB-Datenquelle eingerichtet,
- die Verbindung zu InfluxDB hergestellt,
- das vorbereitete Dashboard geladen,
- die vier benötigten Panels erstellt.

Vagrant stellt zusätzlich die Ubuntu-VM bereit und installiert Docker sowie die für das Lasttest-Skript benötigte Python-Umgebung.

Damit kann die vollständige Umgebung reproduzierbar aufgebaut werden.

---

# Architektur

Die automatisierte Umgebung besteht aus einer mit Vagrant verwalteten Ubuntu-VM. Innerhalb dieser VM werden InfluxDB und Grafana über Docker Compose betrieben.

Der Lasttest wird über ein Python-Skript ausgeführt und greift über den veröffentlichten Port `8086` auf den InfluxDB-Container zu.

```text
                    Hostsystem
                        │
                        │ Vagrant
                        ▼
                ┌─────────────────┐
                │   Ubuntu VM     │
                │                 │
                │  Python-Skript  │
                │       │         │
                │       │ Lasttest│
                │       ▼         │
                │ ┌─────────────┐ │
                │ │  InfluxDB   │ │
                │ │   Docker    │ │
                │ └──────┬──────┘ │
                │        │        │
                │        │ Flux   │
                │        ▼        │
                │ ┌─────────────┐ │
                │ │   Grafana   │ │
                │ │   Docker    │ │
                │ └─────────────┘ │
                └─────────────────┘
                        │
             ┌──────────┴──────────┐
             │                     │
        localhost:8086        localhost:3000
          InfluxDB               Grafana
```

## Datenfluss

Der Datenfluss des Lasttests ist:

```text
Python-Lasttest
      │
      │ Flux-Abfragen
      ▼
   InfluxDB
      │
      │ Lasttest-Ergebnisse
      ▼
Bucket "LoadTest"
      │
      │ Flux
      ▼
    Grafana
      │
      ▼
   Dashboard
```

Das Python-Skript erzeugt die Last und schreibt die gemessenen Ergebnisse zurück in InfluxDB. Grafana liest diese Messwerte aus und stellt sie grafisch dar.

---

# Funktionsumfang

| Funktion | Modularbeit 1 | Modularbeit 2 |
| --- | :---: | :---: |
| Ubuntu-VM mit Vagrant | ✓ | ✓ |
| Installation von InfluxDB | ✓ | ✓ |
| Konfiguration von Organisation und Bucket | ✓ | ✓ |
| API-Zugriff mit Token | ✓ | ✓ |
| Python-Lasttest | ✓ | ✓ |
| Parallele Requests | ✓ | ✓ |
| Messung der Antwortzeiten | ✓ | ✓ |
| Erfassung von Fehlern | ✓ | ✓ |
| Speicherung der Lasttest-Ergebnisse | ✓ | ✓ |
| Grafische Auswertung mit Grafana | – | ✓ |
| InfluxDB als Grafana-Datenquelle | – | ✓ |
| Automatisches Grafana-Provisioning | – | ✓ |
| Automatisches Dashboard | – | ✓ |
| Containerbetrieb mit Docker Compose | – | ✓ |
| Automatisierter Aufbau mit Vagrant | – | ✓ |

---

# Komponenten

| Komponente | Aufgabe |
| --- | --- |
| **InfluxDB** | Speichert die Zeitreihendaten und die Ergebnisse des Lasttests. |
| **Grafana** | Visualisiert die in InfluxDB gespeicherten Lasttest-Ergebnisse. |
| **Python** | Führt den kontrollierten Lasttest gegen InfluxDB aus. |
| **Requests** | Python-Bibliothek für die HTTP-Anfragen an die InfluxDB-API. |
| **Docker Compose** | Erstellt, startet und verwaltet InfluxDB und Grafana. |
| **Vagrant** | Erstellt und provisioniert die Ubuntu-VM und bereitet die Testumgebung vor. |
| **VirtualBox / Parallels** | Dienen als Virtualisierungsprovider für die Vagrant-VM. |

---

# Wieso diese Technologieauswahl

Die Technologien wurden so gewählt, dass sich die Umgebung einfach aufbauen, testen und reproduzieren lässt.

| Verwendete Technologie | Mögliche Alternative | Begründung der Auswahl |
| --- | --- | --- |
| **InfluxDB** | PostgreSQL / TimescaleDB | InfluxDB ist speziell für Zeitreihendaten ausgelegt und eignet sich gut für Mess- und Monitoringdaten. |
| **Grafana** | Kibana | Grafana unterstützt InfluxDB direkt und eignet sich sehr gut zur Visualisierung von Zeitreihendaten. |
| **Python** | Bash | Python ermöglicht parallele HTTP-Anfragen und eine einfache Berechnung von Antwortzeiten und statistischen Kennzahlen. |
| **Docker Compose** | Kubernetes | Für zwei Container innerhalb einer Laborumgebung ist Docker Compose wesentlich einfacher und übersichtlicher. |
| **Vagrant** | Manuell erstellte VM | Vagrant automatisiert die Erstellung und Konfiguration der virtuellen Maschine und verbessert damit die Reproduzierbarkeit. |
| **VirtualBox / Parallels** | VMware | Beide Provider lassen sich mit Vagrant verwenden und ermöglichen den Betrieb der gleichen Laborumgebung auf unterschiedlichen Hostsystemen. |

---

# Voraussetzungen

Für den Betrieb der Umgebung werden benötigt:

- Git
- Vagrant 2.4 oder neuer
- VirtualBox 7.x oder Parallels Desktop
- bei Parallels das Plugin `vagrant-parallels`
- aktivierte Hardware-Virtualisierung
- mindestens 4 GB freier Arbeitsspeicher
- ungefähr 10 GB freier Speicherplatz
- Internetzugang beim ersten Start

Für Parallels kann das benötigte Vagrant-Plugin mit folgendem Befehl installiert werden:

```bash
vagrant plugin install vagrant-parallels
```

---

# Projektstruktur

Die Projektstruktur ist folgendermassen aufgebaut:

```text
Cybersecurity_Lastentest_Teko/
├── README.md
├── .env
├── .env.example
├── docker-compose.yml
├── influx_loadtest.py
│
├── grafana/
│   ├── dashboards/
│   │   └── loadtest-dashboard.json
│   │
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboards.yml
│       │
│       └── datasources/
│           └── influxdb.yml
│
└── lastentest_vm/
    ├── Vagrantfile
    └── scripts/
        ├── system.sh
        ├── docker.sh
        ├── tools.sh
        └── stack.sh
```

Die Datei `.env` enthält Zugangsdaten und den InfluxDB-Token und sollte deshalb nicht in Git gespeichert werden.

---

# Umgebungsvariablen

InfluxDB und Grafana werden über eine `.env`-Datei konfiguriert.

Eine Beispielkonfiguration sieht folgendermassen aus:

```env
INFLUX_USERNAME=admin
INFLUX_PASSWORD=DEIN_PASSWORT
INFLUX_ORG=Iot
INFLUX_BUCKET=LoadTest
INFLUX_TOKEN=DEIN_TOKEN

GRAFANA_USERNAME=admin
GRAFANA_PASSWORD=DEIN_PASSWORT
```

Die Datei `.env` sollte über `.gitignore` vom Git-Repository ausgeschlossen werden.

Stattdessen wird eine `.env.example` als Vorlage im Repository bereitgestellt.

Nach dem Klonen kann daraus eine lokale `.env` erstellt werden:

```bash
cp .env.example .env
```

Anschliessend müssen die gewünschten Zugangsdaten und der InfluxDB-Token eingetragen werden.

---

# Setup und Start

## 1. Repository klonen

Das Repository wird zunächst auf das Hostsystem geklont:

```bash
git clone <repository-url>
```

Anschliessend wird in das Projektverzeichnis gewechselt:

```bash
cd Cybersecurity_Lastentest_Teko
```

## 2. Umgebungsdatei erstellen

Die Beispielkonfiguration wird kopiert:

```bash
cp .env.example .env
```

Anschliessend können die Werte in `.env` angepasst werden.

## 3. In das Vagrant-Verzeichnis wechseln

```bash
cd lastentest_vm
```

## 4. VM starten

Die vollständige Umgebung wird mit folgendem Befehl gestartet:

```bash
vagrant up
```

Vagrant erstellt die Ubuntu-VM und führt die Provisioning-Skripte aus.

Dabei werden:

1. die Ubuntu-VM vorbereitet,
2. Docker installiert,
3. die benötigten Python-Werkzeuge installiert,
4. das Projekt in die VM eingebunden beziehungsweise synchronisiert,
5. InfluxDB gestartet,
6. Grafana gestartet,
7. die InfluxDB-Datenquelle in Grafana eingerichtet,
8. das Grafana-Dashboard bereitgestellt.

Beim ersten Start müssen die Vagrant-Box und die Docker-Images heruntergeladen werden. Deshalb kann der erste Aufbau mehrere Minuten dauern.

---

# Provider auswählen

## VirtualBox

Soll VirtualBox ausdrücklich als Provider verwendet werden:

```bash
vagrant up --provider=virtualbox
```

## Parallels

Soll Parallels ausdrücklich als Provider verwendet werden:

```bash
vagrant up --provider=parallels
```

---

# Status der Umgebung prüfen

## Vagrant-Status

Der Status der VM kann mit folgendem Befehl geprüft werden:

```bash
vagrant status
```

## SSH-Verbindung herstellen

```bash
vagrant ssh
```

## In das Projektverzeichnis wechseln

Innerhalb der VM:

```bash
cd /project
```

## Docker-Container prüfen

```bash
docker compose ps
```

InfluxDB und Grafana sollten beide laufen und einen gesunden Status besitzen.

Beispiel:

```text
NAME       STATUS
InfluxDB   Up (healthy)
Grafana    Up (healthy)
```

---

# Zugriff auf die Dienste

| Dienst | Adresse | Aufgabe |
| --- | --- | --- |
| InfluxDB | `http://localhost:8086` | Speicherung und Abfrage der Messwerte |
| Grafana | `http://localhost:3000` | Visualisierung des Lasttests |

Die Zugangsdaten werden über die `.env`-Datei definiert.

---

# Automatische InfluxDB-Konfiguration

InfluxDB wird beim ersten Start des Containers automatisch eingerichtet.

Docker Compose verwendet dazu folgende Umgebungsvariablen:

```text
INFLUX_USERNAME
INFLUX_PASSWORD
INFLUX_ORG
INFLUX_BUCKET
INFLUX_TOKEN
```

Der für den Lasttest verwendete Bucket ist:

```text
LoadTest
```

Die Messwerte des Lasttests werden unter folgendem Measurement gespeichert:

```text
loadtest
```

---

# Automatische Grafana-Konfiguration

Grafana wird beim Containerstart über Provisioning konfiguriert.

Die InfluxDB-Datenquelle befindet sich unter:

```text
grafana/provisioning/datasources/influxdb.yml
```

Dadurch wird InfluxDB automatisch als Datenquelle in Grafana eingerichtet.

Innerhalb des Docker-Netzwerks verwendet Grafana folgende Adresse:

```text
http://InfluxDB:8086
```

Grafana verwendet dabei die in `.env` definierten Werte für Organisation, Bucket und Token.

Eine manuelle Einrichtung der Datenquelle ist dadurch nach einem Neuaufbau nicht mehr notwendig.

---

# Automatisches Grafana-Dashboard

Das Dashboard wird automatisch über Grafana Provisioning geladen.

Die Provisioning-Konfiguration befindet sich unter:

```text
grafana/provisioning/dashboards/dashboards.yml
```

Das eigentliche Dashboard befindet sich unter:

```text
grafana/dashboards/loadtest-dashboard.json
```

Beim Start von Grafana wird diese Datei automatisch eingelesen.

Das Dashboard enthält vier zentrale Panels:

| Panel | Bedeutung |
| --- | --- |
| **Requests** | Anzahl der ausgeführten Requests |
| **Durchschnittliche Antwortzeit** | Durchschnittliche Antwortzeit der InfluxDB-Abfragen in Millisekunden |
| **Fehler** | Anzahl fehlgeschlagener Requests |
| **P95 Antwortzeit** | Antwortzeit, unterhalb der 95 % der gemessenen Requests liegen |

Damit ist nach einem Neuaufbau der Umgebung keine manuelle Erstellung des Dashboards erforderlich.

---

# Lasttest ausführen

Der Lasttest befindet sich in:

```text
influx_loadtest.py
```

## Mit der VM verbinden

Im Verzeichnis `lastentest_vm`:

```bash
vagrant ssh
```

## In das Projektverzeichnis wechseln

```bash
cd /project
```

## Kleinen Lasttest starten

Für einen ersten Funktionstest:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Dabei werden 100 Requests mit maximal 10 parallelen Workern ausgeführt.

## Grösseren Lasttest starten

Beispielsweise:

```bash
python3 influx_loadtest.py --requests 5000 --workers 50
```

Die Anzahl der Requests und Worker sollte kontrolliert erhöht werden.

---

# Funktionsweise des Lasttests

Das Python-Skript sendet parallele Flux-Abfragen an die lokale InfluxDB-Schnittstelle:

```text
http://localhost:8086
```

Da Docker den Port `8086` des InfluxDB-Containers an die VM weiterleitet, erreichen diese Requests direkt den InfluxDB-Container.

Der Ablauf ist:

```text
influx_loadtest.py
       │
       ├── startet parallele Requests
       │
       ▼
    InfluxDB
       │
       ├── beantwortet Flux-Abfragen
       │
       ▼
Python misst Antwortzeiten
       │
       ├── berechnet Statistiken
       │
       ▼
Bucket "LoadTest"
       │
       ▼
     Grafana
```

Nach Abschluss des Tests werden die Ergebnisse zusätzlich im Terminal ausgegeben.

Beispiel:

```text
Requests:      100
Erfolgreich:   100
Fehler:        0
Ø Antwortzeit: 15.32 ms
P95:           24.81 ms
```

---

# Messwerte des Lasttests

Das Skript schreibt folgende Messwerte nach InfluxDB:

```text
requests
successes
errors
avg_latency_ms
p95_latency_ms
```

Diese Werte bilden die Grundlage für das Grafana-Dashboard.

## Requests

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "requests")
```

## Durchschnittliche Antwortzeit

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "avg_latency_ms")
```

## Fehler

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "errors")
```

## P95-Antwortzeit

```flux
from(bucket: "LoadTest")
  |> range(start: v.timeRangeStart)
  |> filter(fn: (r) => r._measurement == "loadtest")
  |> filter(fn: (r) => r._field == "p95_latency_ms")
```

---

# Interpretation der Ergebnisse

Die durchschnittliche Antwortzeit zeigt, wie schnell InfluxDB die Requests während des Tests im Mittel beantwortet.

Die P95-Antwortzeit ist besonders hilfreich, um langsamere Requests sichtbar zu machen. Ein P95-Wert von beispielsweise `100 ms` bedeutet, dass 95 % der gemessenen Requests innerhalb von ungefähr 100 Millisekunden beantwortet wurden.

Die Fehlerzahl zeigt, ob InfluxDB bei der gewählten Belastung Requests nicht mehr erfolgreich beantworten konnte.

Durch Tests mit unterschiedlichen Worker-Zahlen kann beobachtet werden, wie sich eine steigende Parallelität auf die Datenbank auswirkt.

## Beispiel mit 10 Workern

```bash
python3 influx_loadtest.py --requests 1000 --workers 10
```

## Beispiel mit 25 Workern

```bash
python3 influx_loadtest.py --requests 1000 --workers 25
```

## Beispiel mit 50 Workern

```bash
python3 influx_loadtest.py --requests 1000 --workers 50
```

## Beispiel mit 100 Workern

```bash
python3 influx_loadtest.py --requests 1000 --workers 100
```

Die Ergebnisse können anschliessend im Grafana-Dashboard miteinander verglichen werden.

---
# Testen der beiden Modularbeiten

Die beiden Modularbeiten können getrennt voneinander getestet werden. Dadurch lässt sich nachvollziehen, ob sowohl der Lasttest mit InfluxDB als auch die Visualisierung und Automatisierung mit Grafana korrekt funktionieren.

## Modularbeit 1 – InfluxDB und Lasttest testen

Bei der ersten Modularbeit wird geprüft, ob InfluxDB erreichbar ist und ob das Python-Skript erfolgreich einen Lasttest durchführen und die Ergebnisse in InfluxDB speichern kann.

### 1. VM starten

Zuerst wird in das Verzeichnis der Vagrant-VM gewechselt:

```bash
cd lastentest_vm
```

Danach wird die VM gestartet:

```bash
vagrant up
```

### 2. Verbindung zur VM herstellen

Nach erfolgreichem Start wird eine SSH-Verbindung zur VM hergestellt:

```bash
vagrant ssh
```

Innerhalb der VM wird in das Projektverzeichnis gewechselt:

```bash
cd /project
```

### 3. InfluxDB prüfen

Zuerst wird kontrolliert, ob der InfluxDB-Container läuft:

```bash
docker compose ps
```

Der Container `InfluxDB` sollte den Status `Up` beziehungsweise `healthy` besitzen.

Zusätzlich kann der Health-Endpunkt von InfluxDB geprüft werden:

```bash
curl http://localhost:8086/health
```

InfluxDB sollte dabei einen erfolgreichen Status zurückgeben.

### 4. Lasttest durchführen

Für einen kleinen Funktionstest werden beispielsweise 100 Requests mit 10 parallelen Workern ausgeführt:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Nach Abschluss des Tests sollte im Terminal eine Zusammenfassung erscheinen.

Beispiel:

```text
Requests:      100
Erfolgreich:   100
Fehler:        0
Ø Antwortzeit: 15.32 ms
P95:           24.81 ms
```

Damit ist bestätigt, dass das Python-Skript Requests gegen InfluxDB ausführen und die Antwortzeiten messen kann.

### 5. Gespeicherte Messwerte kontrollieren

Anschliessend kann InfluxDB im Browser geöffnet werden:

```text
http://localhost:8086
```

Im Bucket `LoadTest` sollten Messwerte mit dem Measurement `loadtest` vorhanden sein.

Dabei werden unter anderem folgende Felder gespeichert:

```text
requests
successes
errors
avg_latency_ms
p95_latency_ms
```

Sind diese Messwerte vorhanden, ist die Funktion der **Modularbeit 1 erfolgreich getestet**.

---

## Modularbeit 2 – Grafana und Automatisierung testen

Bei der zweiten Modularbeit wird geprüft, ob Grafana automatisch gestartet wird, InfluxDB automatisch als Datenquelle erhält und das vorbereitete Dashboard ohne manuelle Konfiguration zur Verfügung steht.

### 1. Containerstatus prüfen

Innerhalb der VM wird zunächst kontrolliert, ob InfluxDB und Grafana laufen:

```bash
cd /project
```

Danach:

```bash
docker compose ps
```

Die Container `InfluxDB` und `Grafana` sollten beide laufen und einen gesunden Status besitzen.

### 2. Automatisch erstellte Datasource prüfen

Es kann kontrolliert werden, ob die Provisioning-Datei für InfluxDB im Grafana-Container vorhanden ist:

```bash
docker exec Grafana ls -la /etc/grafana/provisioning/datasources/
```

Dort sollte die Datei für die InfluxDB-Datenquelle sichtbar sein.

Damit kann überprüft werden, ob das Grafana-Provisioning korrekt in den Container eingebunden wurde.

### 3. Automatisch bereitgestelltes Dashboard prüfen

Danach wird geprüft, ob die Dashboard-Datei im Grafana-Container vorhanden ist:

```bash
docker exec Grafana ls -la /var/lib/grafana/dashboards/
```

Dort sollte folgende Datei sichtbar sein:

```text
loadtest-dashboard.json
```

### 4. Grafana im Browser öffnen

Grafana kann auf dem Hostsystem über folgende Adresse geöffnet werden:

```text
http://localhost:3000
```

Nach der Anmeldung sollte InfluxDB bereits als Datenquelle vorhanden sein.

Das vorbereitete Lasttest-Dashboard sollte ebenfalls automatisch verfügbar sein und die vier vorgesehenen Messwerte darstellen:

- Requests
- durchschnittliche Antwortzeit
- Fehler
- P95-Antwortzeit

Eine manuelle Erstellung der Datenquelle oder des Dashboards sollte nicht notwendig sein.

### 5. Dashboard mit einem Lasttest prüfen

Damit Daten im Dashboard sichtbar werden, wird erneut ein Lasttest durchgeführt:

```bash
python3 influx_loadtest.py --requests 1000 --workers 25
```

Anschliessend wird das Grafana-Dashboard geöffnet beziehungsweise aktualisiert.

Die neuen Messwerte sollten automatisch im Dashboard erscheinen.

Damit ist bestätigt, dass die Kette

```text
Python-Lasttest → InfluxDB → Grafana → Dashboard
```

funktioniert.

---

## Vollständige Automatisierung testen

Zusätzlich kann geprüft werden, ob sich die gesamte Umgebung ohne manuelle Installation neu erstellen lässt.

> **Achtung:** Dieser Test löscht die bestehende Vagrant-VM und die darin gespeicherten Docker-Daten.

Zuerst wird die bestehende VM entfernt:

```bash
vagrant destroy -f
```

Danach wird die Umgebung vollständig neu aufgebaut:

```bash
vagrant up
```

Nach erfolgreichem Aufbau wird eine Verbindung zur VM hergestellt:

```bash
vagrant ssh
```

Danach wird in das Projektverzeichnis gewechselt:

```bash
cd /project
```

Der Containerstatus wird geprüft:

```bash
docker compose ps
```

Anschliessend kann ein neuer Lasttest gestartet werden:

```bash
python3 influx_loadtest.py --requests 100 --workers 10
```

Wenn InfluxDB und Grafana automatisch gestartet werden, die Grafana-Datenquelle und das Dashboard automatisch vorhanden sind und der Lasttest erfolgreich durchgeführt werden kann, ist die vollständige Automatisierung des Projekts erfolgreich getestet.

## Erwartetes Testergebnis

| Test | Erwartetes Ergebnis |
| --- | --- |
| InfluxDB-Container | Läuft und ist `healthy` |
| InfluxDB Health Check | Erfolgreiche Antwort |
| Python-Lasttest | Requests werden ausgeführt |
| Speicherung | Messwerte erscheinen im Bucket `LoadTest` |
| Grafana-Container | Läuft und ist `healthy` |
| Grafana-Datenquelle | InfluxDB ist automatisch eingerichtet |
| Grafana-Dashboard | Dashboard ist automatisch vorhanden |
| Visualisierung | Neue Lasttest-Daten erscheinen im Dashboard |
| Neuaufbau mit Vagrant | Umgebung wird mit `vagrant up` automatisch erstellt |


# Entwicklung von manuell zu automatisiert

Ein wichtiger Bestandteil des Projekts war nicht nur die fertige Umgebung, sondern auch deren schrittweiser Aufbau.

## 1. Manueller Aufbau von InfluxDB

InfluxDB wurde zunächst manuell installiert und konfiguriert.

Dabei wurden:

- InfluxDB installiert,
- der Dienst gestartet,
- eine Organisation angelegt,
- ein Bucket erstellt,
- ein API-Token erzeugt,
- die API-Verbindung getestet.

## 2. Entwicklung des Lasttest-Skripts

Anschliessend wurde das Python-Skript entwickelt und gegen die manuell installierte InfluxDB getestet.

Damit konnte überprüft werden, ob:

- parallele Requests funktionieren,
- Antwortzeiten gemessen werden,
- Fehler erkannt werden,
- Ergebnisse wieder in InfluxDB geschrieben werden.

## 3. Manueller Aufbau von Grafana

Grafana wurde zunächst ebenfalls manuell installiert.

InfluxDB wurde manuell als Datenquelle hinterlegt und die benötigten Flux-Abfragen wurden in Grafana erstellt.

Dadurch konnte überprüft werden, welche Daten für das Dashboard benötigt werden.

## 4. Automatisierung mit Docker Compose

Nachdem die manuelle Umgebung funktionierte, wurden InfluxDB und Grafana in Docker-Container überführt.

Docker Compose übernimmt seitdem:

- Start von InfluxDB,
- Initialisierung von InfluxDB,
- Start von Grafana,
- persistente Docker-Volumes,
- Netzwerkkommunikation zwischen den Containern.

## 5. Automatisierung von Grafana

Im nächsten Schritt wurde Grafana Provisioning verwendet.

Damit werden automatisch:

- die InfluxDB-Datenquelle,
- die Verbindungseinstellungen,
- das Lasttest-Dashboard,
- die vier Dashboard-Panels

bereitgestellt.

## 6. Automatisierung mit Vagrant

Vagrant bildet die letzte Automatisierungsstufe.

Die vollständige Umgebung kann mit folgendem Befehl aufgebaut werden:

```bash
vagrant up
```

Das Ziel dieser Entwicklung war, aus einer zunächst manuell eingerichteten Laborumgebung eine reproduzierbare und automatisierte Testumgebung zu erstellen.

---

# Bedienung und Fehlersuche

Die folgenden Vagrant-Befehle werden im Verzeichnis `lastentest_vm` ausgeführt.

## VM-Status anzeigen

```bash
vagrant status
```

## VM starten

```bash
vagrant up
```

## VM herunterfahren

```bash
vagrant halt
```

## SSH-Verbindung herstellen

```bash
vagrant ssh
```

## Provisionierung erneut ausführen

```bash
vagrant provision
```

---

# Docker-Container prüfen

Zuerst mit der VM verbinden:

```bash
vagrant ssh
```

Danach in das Projektverzeichnis wechseln:

```bash
cd /project
```

Containerstatus anzeigen:

```bash
docker compose ps
```

## Logs von InfluxDB anzeigen

```bash
docker logs InfluxDB
```

## Logs von Grafana anzeigen

```bash
docker logs Grafana
```

## Logs aller Compose-Dienste anzeigen

```bash
docker compose logs --tail=100
```

---

# InfluxDB prüfen

Der Health-Endpunkt von InfluxDB kann mit folgendem Befehl getestet werden:

```bash
curl http://localhost:8086/health
```

InfluxDB sollte einen erfolgreichen Status zurückgeben.

---

# Grafana-Provisioning prüfen

## Datasource prüfen

Mit folgendem Befehl kann geprüft werden, ob die InfluxDB-Datenquelle in den Grafana-Container eingebunden wurde:

```bash
docker exec Grafana ls -la /etc/grafana/provisioning/datasources/
```

## Dashboard prüfen

Mit folgendem Befehl kann geprüft werden, ob das Dashboard im Grafana-Container vorhanden ist:

```bash
docker exec Grafana ls -la /var/lib/grafana/dashboards/
```

Dort sollte die Dashboard-Datei sichtbar sein:

```text
loadtest-dashboard.json
```

---

# Besonderheit bei Parallels

Bei Parallels wird das Projekt über RSync in die VM übertragen.

Nach Änderungen am Hostsystem muss deshalb gegebenenfalls erneut synchronisiert werden.

Dazu wird im Verzeichnis `lastentest_vm` folgender Befehl ausgeführt:

```bash
vagrant rsync
```

Anschliessend kann eine SSH-Verbindung zur VM hergestellt werden:

```bash
vagrant ssh
```

Innerhalb der VM wird in das Projektverzeichnis gewechselt:

```bash
cd /project
```

Danach können die Docker-Container neu erstellt werden:

```bash
docker compose up -d --force-recreate
```

Bei VirtualBox kann dagegen ein direkt eingebundener Projektordner verwendet werden. Änderungen am Hostsystem stehen dadurch direkt innerhalb der VM zur Verfügung.

---

# Docker-Dienste neu starten

Falls lediglich die Container neu gestartet werden sollen:

```bash
docker compose restart
```

Falls die Container neu erstellt werden sollen:

```bash
docker compose up -d --force-recreate
```

---

# Docker-Daten vollständig zurücksetzen

Falls die Testumgebung vollständig neu initialisiert werden soll, werden zunächst die Container und Docker-Volumes entfernt:

```bash
docker compose down -v
```

Anschliessend wird die Umgebung neu gestartet:

```bash
docker compose up -d
```

> **Achtung:** Durch das Entfernen der Docker-Volumes gehen die darin gespeicherten InfluxDB- und Grafana-Daten verloren.

Da das Grafana-Dashboard und die Datasource über Provisioning im Projekt gespeichert sind, werden diese beim nächsten Start automatisch wiederhergestellt.

---

# VM vollständig neu erstellen

Falls die komplette virtuelle Maschine gelöscht werden soll:

```bash
vagrant destroy -f
```

Danach kann die VM vollständig neu aufgebaut werden:

```bash
vagrant up
```

Dadurch lässt sich prüfen, ob die Automatisierung des Projekts auch auf einer komplett neuen VM funktioniert.

---

# Git und sensible Daten

Die `.env`-Datei enthält Zugangsdaten und den InfluxDB-Token und sollte deshalb nicht in das Git-Repository aufgenommen werden.

Die `.gitignore` sollte mindestens folgende Einträge enthalten:

```gitignore
.env
venv/
.vagrant/
.DS_Store
```

Statt der echten `.env` wird eine `.env.example` im Repository bereitgestellt.

Dadurch bleibt die benötigte Konfiguration dokumentiert, ohne Zugangsdaten oder Tokens zu veröffentlichen.

Nach dem Klonen wird die Vorlage kopiert:

```bash
cp .env.example .env
```

Anschliessend werden die benötigten Werte lokal eingetragen.

---

# Ausblick

Die bestehende Umgebung kann später erweitert werden.

Mögliche Erweiterungen sind:

- automatische Durchführung mehrerer Laststufen,
- Vergleich verschiedener Worker-Zahlen,
- zusätzliche Kennzahlen wie Minimum, Maximum und Median,
- CPU- und RAM-Monitoring während des Lasttests,
- automatische Grafana-Alerts bei hohen Antwortzeiten,
- automatische Testberichte,
- Vergleich verschiedener InfluxDB-Konfigurationen,
- zusätzliche Dashboards für Systemressourcen.

Damit könnte die bestehende Lasttest-Umgebung zu einer umfangreicheren Monitoring- und Performance-Testplattform erweitert werden.

---

# Sicherheitshinweis

Das Lasttest-Skript erzeugt gezielt eine erhöhte Anzahl von Anfragen.

Es darf deshalb nur gegen die eigene Laborumgebung oder gegen Systeme eingesetzt werden, für die eine ausdrückliche Genehmigung vorliegt.

Eine hohe Anzahl paralleler Requests kann Dienste stark belasten oder zu deren Ausfall führen. Die Anzahl der Requests und Worker sollte deshalb schrittweise erhöht und während des Tests überwacht werden.

Die in diesem Projekt verwendeten Zugangsdaten und Tokens sind ausschliesslich für die isolierte Laborumgebung vorgesehen und dürfen nicht für produktive Systeme übernommen werden.