# temperatur logger

Kleines Projekt um mit dem Raspberry Pi die interne CPU und GPU Temperature und die Temperature eines angeschlossenen 1-wire Temperaturesensors zu loggen. Neben der simplen Messwertaufnahme und Speicherung in einer CSV, werden die Temperaturwerte auch in einer Datenbank abgelegt.Weiterhin können einige Auswertefunktionen relativ einfach genutzt werden. Derzeit habe ich folgende Funktionen implementiert:
* minimal Temperatur
* maximale Temperatur
* durchschnittliche Temperatur
* Einschränkung des Zeitraum der statistischen Auswertung durch Angabe des Start- und Enddatums.

# Inhalt

##cpu_temperature.py
Dieses Skript liest die Temperaturen der GPU, CPU und eines 1-wire Temperatursensors aus. Diese werden anschließend in eine csv Datei und in eine sqlite3 Datenbank geschrieben. Aufgerufen wird das Skript per cronjob. Um das Skript an das eigene Setup anzupassen, kann der Pfad für die CSV und die Datenbank und muss die ID des 1-wire Sensors (siehe  Raspberry Pi 1-wire mit Device Tree Overlay) angepasst werden.

##database_temperature.py 
Dieses Skript hat zwei Einsatzmöglichkeiten. Erstens wird es von cpu_temperature.py zum Speichern der Temperaturwerte in der Datenbank aufgerufen. Zweitens kann dieses alleine dazu genutzt werden die Statistikfunktionen zu nutzen.

```
$./database_temperature.py
usage: database_temperature.py [-h] [-i] [-d DIRECTORY] [--min] [--max]
                               [--avg] [-s START] [-e END] [-p]
optional arguments:
  -h, --help    show this help message and exit
  -i            import all csv files of current dir
  -d DIRECTORY  set working directory
  --min         show mininmal value
  --max         show maximal value
  --avg         show average value
  -s START      set start date YYYY-MM-DD
  -e END        set end date YYYY-MM-DD
  -p            print values
```

##move.sh
Ist ein einfaches Shell Skript, welches ebenfalls per cronjob aufegrufen wird. Der Zweck des Skriptes liegt darin, dass es die CSV Datei des Vortages anhand des Datums umbennet. Als Resultat gibt es für jeden Tag eine CSV mit allen Messwerten.    Wird das Skript nicht verwendet landen alle Messwerte in einer CSV Datei.

##frizing 
Ist ein Ordner und enthält das Frizing Modell aus  Raspberry Pi 1-wire mit Device Tree Overlay.

##dygraph-combined.js, dygraph-extra.js, index.html

Visualisierung der CSV Messdaten mittels dygraph im Browser. Mehr dazu gibt es z.B. hier Datenvisualisierung mit Dygraph.

#Verwendung
Zuerst muss das projekt von github gecloned werden. Dazu zuerst ins HOME Verzeichnis wechseln.

```

$cd ~

$ git clone https://github.com/f0xd3v1lsw1ld/1-wire.git

```

Nachdem nun alle Projektdatein beschrieben sind, erfolgt die Aktivierung der automatischen Messwertaufnahme. Dazu muss crontab geöffnet werden und die folgenden beiden Zeilen (für die Messwertaufnahme und die CSV Umbenennung) eingetragen werden. Evtl. muss der Pfad für die Skripte an des entsprechende Setup angepasst werden.
```
crontab -e 

*/10 * * * * /home/pi/1-wire/cpu_temperature.py>>/dev/null

00 0 * * * /home/pi/1-wire/move.sh /home/pi/1-wire/ rpi_temperature.csv>>/dev/null

```

**Erklärung**

Mit der ersten Zeile wird  cpu_temperature.py alle 10 min aufgerufen und alle evtl. auftretenden Ausgaben nach /dev/null ausgegeben.

Mit der zweiten Zeile wird  move.sh täglich um 00:00 aufgerufen und alle evtl. auftretenden Ausgaben nach /dev/null ausgegeben.
