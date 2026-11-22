# HUMANS. WHY? – Produktionsordner

Kanal: https://www.youtube.com/@HumansWhyAI (Kanal-ID UCbTM9luniU6p1Zub9pdo5JQ)

- `folgen/` – eine JSON-Datei pro Folge (Text, Bilder, Überschriften, Quellen)
- `bilder/` – alle KI-Bilder aus Flow, nach Folge sortiert; `flow/b01.jpg` (Moderator) und `flow/b05.jpg` (Roboter im Orbit) sind die festen Start- und Schlussbilder
- `pipeline/` – `tts.py` (Stimme), `render.py` (Video), `build.sh` (beides)

## Aufbau einer Folge
1. Hook (Ereignis + trockener Satz)
2. 3 bis 5 Themen oder Fragen, je ein Punkt plus ein sarkastischer Nachschlag
3. Schluss: "Why? Because you're human. I'm just the AI. I don't have to live here. You do. Follow ..."

## Zeichen im Sprechtext (`say`)
- `|` kurze Pause, `||` mittlere Pause, `/` Pause vor der Pointe
- `^` am Satzanfang: überrascht (höher, schneller)
- `~` am Satzanfang: enttäuscht (tiefer, langsamer) – für Pointen
- Abkürzungen ausschreiben: "A I", "G T A six", "U F O"

## Bilder pro Thema
`imgs`: Liste der Bilder, `_cuts`: Anteil der Szene (0 bis 1), ab dem das jeweilige Bild kommt. Drei Bilder pro Thema: Aufbau, Pointe, Nachschlag.

## Regeln
- Nur belegte Fakten, Quelle in `src`. Keine erfundenen Zitate. Keine Witze über Krieg und Tote.
- Bilder ohne Text, Logos, echte Personen. Hinweis "AI-generated images and voice" bleibt im Bild.
- Nichts wird ohne Freigabe von Thomas veröffentlicht.
