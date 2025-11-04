# JSON-Struktur der Reisebausteine (bausteine.json)

## 🧭 Allgemeine Beschreibung
Die Datei enthält alle Textbausteine für die automatische Erstellung von Reiseplänen.
Jeder Eintrag repräsentiert entweder einen Ort (City) oder eine Verbindung (Route).
Beide Typen haben unterschiedliche Pflicht- und optionale Felder.

Diese Trennung ermöglicht:

- sauberen Datenzugriff im Backend (city ≠ route_*)

- klare Validierung in Tests

- einfachere Erweiterung um neue Typen (z. B. intro, outro)

### Gemeinsame Basisfelder
```json
{
  "id": "string",         // eindeutige Kennung des Bausteins
  "type": "string",       // Typ des Bausteins: city, route_simple, route_detailed, intro, outro
  "title": "string",      // Titel oder Überschrift
  "text": "string"        // Haupttext oder Beschreibung
}
```

## 🏙️ City-Baustein (Orte)
**Zweck**: Repräsentiert eine Stadt oder einen Aufenthaltsort im Reiseplan.
Enthält ortsspezifische Informationen, Sehenswürdigkeiten und optional ein Bild.

**Pflichtfelder:**  
`id, type, title, text, ort`

**Optionale Felder:**  
``sehenswuerdigkeiten, image``

**Nicht erlaubt:**  
``start_ort, ziel_ort, varianten``

### Beispiel: City-Baustein
```json
{
  "id": "city_kopenhagen",
  "type": "city",
  "title": "Kopenhagen",
  "text": "Kopenhagen – die Hauptstadt Dänemarks ...",
  "ort": "Kopenhagen",
  "sehenswuerdigkeiten": ["Tivoli", "Nyhavn"],
  "image": "nyhavn.jpg"
}
```

## 🛣️ Route-Baustein (Verbindungen)
**Zweck:** Beschreibt eine Reiseverbindung zwischen zwei Orten.
Verknüpft Start- und Zielorte, optional mit Varianten und Zwischenstopps.

**Pflichtfelder:**  
``id, type, title, text, start_ort, ziel_ort``

**Optionale Felder:**  
``varianten, sehenswuerdigkeiten, image``

**Nicht erlaubt:**  
``ort``

### Beispiel: Einfache route
```json
{
  "id": "route_stege_kopenhagen",
  "type": "route_simple",
  "title": "Stege - Kopenhagen, ca. 125 km",
  "text": "Direkte Route von Stege nach Kopenhagen über die E47.",
  "start_ort": "Stege",
  "ziel_ort": "Kopenhagen"
}
```
### Beispiel: Detaillierte Route
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

## 🧪 Validierungslogik (Tests)
- **Jede Route** muss auf existierende City-Orte verweisen (``start_ort, ziel_ort in cities``).
- **Keine City** darf ``start_ort oder ziel_ort`` enthalten.
- **Der Graph** aus allen Routen muss gültige Nachbarn enthalten (keine Sackgassen ohne Ziel).