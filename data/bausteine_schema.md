# JSON-Struktur der Reisebausteine (bausteine.json)

## Allgemeine Beschreibung
Die Datei enthält Textbausteine für die automatische Erstellung von Reiseplänen.
Jeder Eintrag repräsentiert einen Baustein (Ort, Route oder Abschnitt) und besitzt einheitliche Felder.
Nicht benötigte Felder können leer oder null sein.

---

## Basisstruktur
```json
{
  "id": "string",               // eindeutige Kennung des Bausteins
  "type": "string",             // Typ des Bausteins: intro, city, route_simple, route_detailed, outro
  "title": "string",            // Überschrift oder Kurzbeschreibung
  "text": "string",             // Haupttext des Abschnitts
  "ort": "string | null",       // Ort (nur bei city)
  "start_ort": "string | null", // Startpunkt (nur bei route)
  "ziel_ort": "string | null",  // Zielpunkt (nur bei route)
  "varianten": [                // nur bei route_detailed
    {
      "name": "string",
      "beschreibung": "string",
      "zwischenstopps": [
        {
          "ort": "string",
          "highlight": "string",
          "details": "string"
        }
      ]
    }
  ],
  "sehenswuerdigkeiten": [      // optional, meist bei city oder route_simple
    "string"
  ],
  "image": "string | null"      // Dateiname oder Pfad zum Bild
}
```
---

## Beispiel: City-Baustein
```json
{
  "id": "city_kopenhagen",
  "type": "city",
  "title": "Kopenhagen",
  "text": "Kopenhagen - die Hauptstadt Dänemarks ...",
  "ort": "Kopenhagen",
  "start_ort": null,
  "ziel_ort": null,
  "varianten": null,
  "sehenswuerdigkeiten": ["Tivoli", "Nyhavn"],
  "image": "nyhavn.jpg"
}
```
---

## Beispiel: Detaillierte Route
```json
{
  "id": "route_malmo_kopenhagen",
  "type": "route_detailed",
  "title": "Malmö - Kopenhagen, ca. 45 km",
  "start_ort": "Malmö",
  "ziel_ort": "Kopenhagen",
  "varianten": [
    {
      "name": "Direkte Route über die Oresundbrücke",
      "beschreibung": "Über die E20 ...",
      "zwischenstopps": [
        {"ort": "Kastrup", "highlight": "Den Bla Planet", "details": "Aquarium am Meer"}
      ]
    }
  ]
}
```
