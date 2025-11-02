# Smart Recycle Bot Project

## 🚀 Teil 1: Abgabe-Template - Inhaltliche Abgabe (40 Punkte)

Bitte beantworten Sie die folgenden Abschnitte in vollständigen Sätzen.
Jede Antwort 7–10 Zeilen (nicht nur Stichpunkte, sondern Sätze).
README.md soll am Ende max. 220 Zeilen haben.

1. Executive Summary – Kurze Zusammenfassung des Projekts.  
2. Ziele des Projekts – Welche Ziele verfolgt Ihr Projekt, welches Problem wird gelöst?  
3. Anwendung und Nutzung – Wie wird die Lösung verwendet, wer sind die Hauptnutzer:innen?  
   - Hier bitte auch den Link zum Code-Repository und zum Pitch (Audio bevorzugt, alternativ Video) einfügen.  
4. Entwicklungsstand – Idee, Proof of Concept, Prototyp oder Einsatzbereit?  
5. Projektdetails – Welche Kernfunktionen oder Besonderheiten bietet Ihr Projekt?  
6. Innovation – Was ist neu und besonders innovativ?  
7. Wirkung (Impact) – Welchen konkreten Nutzen bringt Ihr Projekt?  
8. Technische Exzellenz – Welche Technologien, Daten oder Algorithmen werden genutzt?  
9. Ethik, Transparenz und Inklusion – Wie stellen Sie Fairness, Transparenz und Sicherheit sicher?  
10. Zukunftsvision – Wie könnte das Projekt in 5–10 Jahren aussehen?  

## 🚀 Teil 2: Technische Umsetzung (60 Punkte)

1. **AI-Komponente (25 Punkte)**  
   - Mindestens eine Funktion (z. B. Zusammenfassung, Empfehlung, Chat).  
   - Nutzung einer API (z. B. Deepseek, OpenAI) erlaubt. (Key"s werden vom Dozent bereitgestellt) 
   - Antworten sollen verlässlich sein: lieber „weiß ich nicht“ als falsche Antworten. Wenig wie möglich Halluzinationen der AI.  
   - Für alle Projekte dürfen **Dummy-Daten oder simulierte Daten** verwendet werden. Wichtig ist, dass die Funktionsweise der AI **klar nachvollziehbar** gezeigt wird – auch ohne Live-Daten.

2. **Docker (20 Punkte)**  
   - App containerisieren (Dockerfile).  
   - Lokal startbar mit `docker compose up -d`.  

3. **Kubernetes (10 Punkte)** 
   - lokal, kind
   - Kubernetes-Manifeste im Ordner `k8s/` mit mindestens 2 Services (z. B. api ).  
   - Mindestens ein Deployment pro Service.  
   - Nur API-Endpunkte, keine grafische Oberfläche notwendig. 

4. **Pitch (5 Punkte)**  
   - Audio bevorzugt, alternativ Video, max. 25 MB
   - Dauer: 1–3 Minuten.  
   - Kann im Code-Repository enthalten sein.   

## 🚀 To-do-Liste  

1. Thema wählen (aus den Kategorien).  
2. AI-Komponente bauen.  
3. App in Docker packen (Dockerfile).  
4. k8s Cluster in Docker starten.  
5. Services in Kubernetes deployen (Ordner `k8s/`).  
6. Pitch aufnehmen (Audio bevorzugt, alternativ Video, 1–3 Minuten).  
7. Finale Kontrolle: README.md (10 Fragen) und nicht mehr als 220 Zeilen, Code, Kubernetes, Pitch vollständig. Per E-mail an alkurdiz@htw-berlin.de bis 23:59:59 Uhr am 22.11.2025!