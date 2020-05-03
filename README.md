# Anki Deck Generator

Generiert [Anki](https://apps.ankiweb.net/) Deck Karten für die [FernUniversität in Hagen](https://fernuni-hagen.de/) Kurse.

Die zuletzt automatisch generierten Decks sind unter [Releases](https://github.com/nh-hagen/FernUni-Anki/releases/tag/latest) zu finden.

## Generierung
### Python
Die csv Dateien werden mit einem Ptyhon3 Skript ins Anki Format übertragen.
```
pip3 install genanki
python3 generate.py
```
Danach lassen sich die apkg Dateien in Anki importieren.

### Docker
Ist auf dem (Linux) System schon [Docker](https://docker.com) installiert, genügt folgender Aufruf:
```
docker run --rm -ti -v "$PWD:/anki" -u $UID python:3-alpine sh -c "pip install --prefix /tmp genanki && cd /anki && PYTHONUSERBASE=/tmp python generate.py"
```

Dafür gibt es auch

```
./generate.sh
```

## Mitmachen
### csv Dateien
csv Dateien sollten im Schema "\<Kursnummer\> \<Kursbezeichnung\>/\<Kurseinheit\>/basic.csv" benannt werden

Die Dateien sind mit dem Seperator ";" (Semikolon) getrennt
```
Vorderseite;Rückseite
```

### Bilder
Bilder sollten unter "\<Kursnummer\> \<Kursbezeichnung\>/images" abgelegt werden und können in Karten mit ```<img src="foo.jpg">``` verwendet werden. (Ohne Verzeichnis "images")
