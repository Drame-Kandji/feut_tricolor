# 🚦 Simulation de régulation de la circulation

Projet POO2 – Licence 3 Informatique (2025–2026)

## 🎯 Objectif
Simuler un carrefour urbain avec feux tricolores, véhicules autonomes, scénarios de trafic et journalisation SQLite.

---

## ✅ Fonctionnalités principales
- Feux tricolores automatiques et mode manuel
- 3 scénarios: normale, pointe, nuit
- Véhicules avec gestion de collisions et distance de sécurité
- Interface graphique (Turtle + Tkinter)
- Base de données SQLite pour journaliser les événements
- Images GIF possibles pour voitures réalistes

---

## 🧱 Architecture (modules)
- `main.py` : point d’entrée + boucle principale
- `vehicles.py` : classe Vehicle (mouvement, collisions)
- `traffic_light.py` : logique des feux tricolores
- `scenarios.py` : scénarios de circulation
- `turtle_scene.py` : dessin du carrefour
- `gui.py` : sidebar et boutons
- `database.py` : enregistrement SQLite
- `logger.py` : collisions et violations

---

## 🖥️ Installation
### Prérequis
- Python 3.8+
- Tkinter (déjà inclus sous Windows / macOS)

### Linux (Ubuntu/Debian)
```bash
sudo apt install python3-tk
```

---

## ▶️ Lancer la simulation
Depuis le dossier du projet:
```bash
python3 main.py
```

---

## 🕹️ Contrôles (interface)
- START : démarrer
- PAUSE : pause / reprise
- STOP : arrêt
- RESET : réinitialisation
- NORMALE / POINTE / NUIT : scénarios
- MANUEL : bascule des feux

---

## 🚗 Ajouter des voitures réelles (GIF)
1. Placer des GIF dans le dossier `images/` (ex: car_red.gif)
2. Taille recommandée : 40×20 ou 50×25
3. Vue de dessus (top view)
4. Fond transparent si possible

Le code peut être ajusté dans `vehicles.py` pour charger automatiquement ces GIF.

---

## 🗃️ Base de données
Un fichier `simulation_trafic.db` est créé automatiquement.
Tables principales:
- evenements
- changements_feu_tricolore
- collisions
- violations

---

## 🧪 Astuces rapides
- Trop de collisions ? Augmenter `distance_securite` dans `scenarios.py`
- Simulation lente ? Réduire le nombre de véhicules
- Images trop grandes ? Redimensionner les GIF

---

## 📁 Structure du projet
```
project_feu_tricolore/
├── main.py
├── vehicles.py
├── traffic_light.py
├── scenarios.py
├── turtle_scene.py
├── gui.py
├── database.py
├── logger.py
├── images/
└── simulation_trafic.db
```

---

## 👨‍🎓 Auteur
Projet réalisé dans le cadre du module POO2.
