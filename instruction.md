# ♻️ Smart Recycle Bot 

## backend/
- In diesem Ordner befindet sich ein **FastAPI-Backend**, das mithilfe von OpenAI und Qdrant intelligente Antworten zum Thema Mülltrennung und Recycling liefert.
- Der Bot kann sowohl Texteingaben als auch Bilder verarbeiten und liefert passende Entsorgungshinweise.

## frontend/
- In diesem Ordner befindet sich ein **Streamlit-Frontend** des Smart Recycle Bot. Es ermöglicht Nutzer:innen, Abfallgegenstände über Text oder Bilder einzugeben und passende Recycling-Hinweise vom Backend zu erhalten.

## qdrant/
- Dieser Ordner enthält das Skript `main.py`, das eine Qdrant-Collection initialisiert und die aus der CSV-Datei  `qdrant/data/out/abfall_abc_cleaned.csv` vektorisierten Einträge hochlädt.
- Die enthaltene Datei `docker-compose.yml` dient ausschließlich lokalen Tests

## k8s/
- Dieser Ordner enthält Kubernetes Deployment- und Service-Manifestdateien zur Bereitstellung der Smart Recycle Bot-Anwendung in einem Kubernetes-Cluster.

## docker-compose.yml
- Dies ist die erste Möglichkeit, das Projekt auszuführen. 
- Befehl: `docker compose up -d`

## start.ps1
- Dies ist die zweite Möglichkeit, das Projekt auszuführen (mit Kubernetes) 
- Starte zuerst einen K8s-Cluster, öffne Terminal und führe anschließend aus: `.\start.ps1`