"""
Module de gestion de la base de données SQLite
Gère la journalisation de tous les événements de la simulation
"""

import sqlite3
import threading
import queue
from datetime import datetime


class DatabaseManager:
    """Gestionnaire de base de données SQLite pour la journalisation"""
    
    def __init__(self, db_name="simulation_trafic.db"):
        self.db_name = db_name
        self.queue = queue.Queue()
        self.init_database()
        self.start_worker()
    
    def init_database(self):
        """Initialise la base de données et crée les tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Table principale des événements
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evenements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                type_action TEXT NOT NULL,
                action TEXT NOT NULL,
                etat_feu TEXT,
                scenario TEXT,
                id_voiture INTEGER,
                position_x REAL,
                position_y REAL,
                vitesse REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_event(self, type_action, action, **kwargs):
        """Ajoute un événement à la file d'attente"""
        event = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type_action': type_action,
            'action': action,
            **kwargs
        }
        self.queue.put(event)
    
    def _worker(self):
        """Thread worker pour l'écriture asynchrone dans la BD"""
        conn = sqlite3.connect(self.db_name)
        
        while True:
            try:
                event = self.queue.get(timeout=1)
                if event is None:
                    break
                
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO evenements 
                    (timestamp, type_action, action, etat_feu, scenario, id_voiture, position_x, position_y, vitesse)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event.get('timestamp'),
                    event.get('type_action'),
                    event.get('action'),
                    event.get('etat_feu'),
                    event.get('scenario'),
                    event.get('id_voiture'),
                    event.get('position_x'),
                    event.get('position_y'),
                    event.get('vitesse')
                ))
                
                conn.commit()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erreur BD: {e}")
        
        conn.close()
    
    def start_worker(self):
        """Démarre le thread de journalisation"""
        worker_thread = threading.Thread(target=self._worker, daemon=True)
        worker_thread.start()
