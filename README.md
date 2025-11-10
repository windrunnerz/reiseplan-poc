## 🧭 Anleitung

**Hinweis:**  
Beim ersten Aufruf oder nach längerer Inaktivität kann der Server bis zu **eine Minute** benötigen, um zu starten.  

---

### ⚙️ Funktionsweise

Die Anwendung arbeitet **vollautomatisch und intelligent**:  
Sie erkennt alle verfügbaren Routen anhand der gespeicherten Bausteine und erstellt daraus automatisch passende Reisepläne.  

Der erzeugte Reiseplan folgt immer einem festen Schema:

> **City → Route → City → Route → City**

Dabei analysiert die App eigenständig, **welche Orte in welcher Reihenfolge miteinander verbunden sind**,  
und passt den Reiseplan dynamisch an, sobald neue Bausteine hinzukommen.

#### 🧠 Beispiel: intelligente Aktualisierung

Wenn du z. B. eine bestehende Beispielroute hast:
> Stege → Kopenhagen → Aarhus → Vemb

und du zwischen *Stege* und *Kopenhagen* einen neuen Ort samt zwei neuen Routen hinzufügst, z. B.:

> Stege → **Route 1** → Neuer Ort → **Route 2** → Kopenhagen

dann erkennt die Anwendung diese neue Zwischenstation automatisch.  
Der gesamte Reiseplan wird korrekt neu zusammengesetzt, **ohne dass bestehende Daten nachgepflegt werden müssen**.  
Auch alle nachfolgenden Abschnitte (Kopenhagen → Aarhus → Vemb) bleiben erhalten und werden weiterhin berücksichtigt.

---

### 📋 Hintergrund / ersetzter Workflow

Bisher wurde jeder Reiseplan **manuell** erstellt:

1. Die relevanten Orte wurden aus der **Rechnung** entnommen.  
2. Die passenden **Textbausteine** (Einleitung, Reiseabschnitte, Schlussbemerkung) wurden aus einer bestehenden Sammlung gesucht.  
3. Diese Texte wurden in ein neues Dokument kopiert, individuell angepasst und anschließend gespeichert oder gedruckt.

Die neue Anwendung automatisiert diesen Prozess vollständig:

- Alle passenden **City- und Routen-Bausteine** werden automatisch erkannt und zu einem vollständigen Reiseplan zusammengesetzt.  
- **Individuelle Beschreibungen** können beim Anlegen neuer Bausteine direkt hinterlegt werden.  
- Änderungen oder Erweiterungen (z. B. neue Orte oder Zwischenrouten) werden **sofort erkannt** und fließen automatisch in die Reiseplanung ein.  

Das spart Zeit, reduziert Fehlerquellen und stellt sicher, dass alle Texte konsistent und aktuell bleiben.

---

### ✈️ Reiseplan erzeugen

1. **Start-Ort** auswählen  
2. **Ziel-Ort** auswählen  
3. Eine der vorgeschlagenen **Routen** wählen  
4. Auf **„Reiseplan erzeugen“** klicken

💡 *Hinweis:*  
Die Auswahl der Ziel-Orte wird automatisch auf die tatsächlich erreichbaren Ziele beschränkt.  

---

### 🏗️ Neue Bausteine hinzufügen

1. Auf **„Neuen Baustein hinzufügen“** klicken  
2. Zwischen **City** oder **Route** wählen  
3. Optional eine **Beschreibung** eintragen  
4. Mit **„Speichern“** bestätigen

🔹 Neue City- und Routen-Bausteine werden automatisch erkannt.  
🔹 Sie erscheinen sofort in der Auswahl für Start- und Ziel-Orte.    
