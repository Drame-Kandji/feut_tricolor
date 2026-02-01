"""
═══════════════════════════════════════════════════════════════════════════════
    SIMULATION DE RÉGULATION DE LA CIRCULATION ROUTIÈRE AVEC FEUX TRICOLORES
═══════════════════════════════════════════════════════════════════════════════

Université Iba Der Thiam de Thiès
UFR SET / Département Informatique
LICENCE 3, INFO - GL | 2025 – 2026
M. DIOUF / SEMESTRE 5 – POO2 - PROJET

Point d'entrée principal de l'application

UTILISATION:
    python main.py

═══════════════════════════════════════════════════════════════════════════════
"""

import time
import random
import turtle

from database import DatabaseManager
from traffic_light import TrafficLight
from scenarios import CirculationNormale, HeureDePointe, ModeNuit
from vehicles import Vehicle
from turtle_scene import TurtleScene, TrafficLightView
from gui import GUI
from logger import Logger


class Simulation:
    """Classe principale gérant la simulation complète"""
    
    def __init__(self, traffic_light, scenario, db_manager):
        self.traffic_light = traffic_light
        self.scenario = scenario
        self.db_manager = db_manager
        self.logger = Logger(db_manager)
        
        self.vehicles = []
        self.running = False
        self.paused = False
        self.last_spawn_time = time.time()
        self.collisions = 0
        
        # Journalisation
        self.db_manager.log_event('SYSTEME', 'Simulation initialisée', 
                                  scenario=self.scenario.name)
    
    def start(self):
        """Démarre la simulation"""
        if not self.running:
            self.running = True
            self.paused = False
            self.db_manager.log_event('SYSTEME', 'Démarrage simulation')
    
    def pause(self):
        """Met en pause ou reprend la simulation"""
        if not self.running:
            self.start()
        elif self.paused:
            self.paused = False
            self.db_manager.log_event('SYSTEME', 'Reprise simulation')
        else:
            self.paused = True
            self.db_manager.log_event('SYSTEME', 'Pause simulation')
    
    def stop(self):
        """Arrête la simulation"""
        if self.running:
            self.running = False
            self.paused = False
            self.db_manager.log_event('SYSTEME', 'Arrêt simulation')
    
    def reset(self):
        """Réinitialise la simulation"""
        for v in self.vehicles:
            v.hideturtle()
            del v
        self.vehicles = []
        
        self.traffic_light.etat_ns = self.traffic_light.EtatFeu.ROUGE
        self.traffic_light.etat_eo = self.traffic_light.EtatFeu.VERT
        self.traffic_light.phase = "EO"
        self.traffic_light.mode_manuel = False
        
        self.collisions = 0
        self.logger.collision_count = 0
        self.logger.violation_count = 0
        
        self.running = False
        self.paused = False
        
        self.db_manager.log_event('SYSTEME', 'Réinitialisation simulation')
    
    def change_scenario(self, new_scenario):
        """Change le scénario de simulation"""
        old_scenario = self.scenario.name
        self.scenario = new_scenario
        self.traffic_light.last_change = time.time()
        self.traffic_light.set_auto_mode()
        
        # Ajuster le nombre de véhicules
        self._adjust_vehicle_count()
        
        self.db_manager.log_event('SYSTEME', 'Changement de scénario',
                                  scenario=new_scenario.name)
    
    def _adjust_vehicle_count(self):
        """Ajuste le nombre de véhicules selon le scénario"""
        target = self.scenario.nb_vehicules
        
        while len(self.vehicles) < target:
            direction = random.choice(["EST", "OUEST", "NORD", "SUD"])
            vehicle = Vehicle(direction, self.db_manager)
            vehicle.distance_securite = self.scenario.distance_securite
            self.vehicles.append(vehicle)
        
        while len(self.vehicles) > target:
            v = self.vehicles.pop()
            v.hideturtle()
            del v
    
    def update(self):
        """Met à jour l'état de la simulation"""
        if not self.running or self.paused:
            return
        
        # Apparition de nouveaux véhicules
        if self.scenario.should_spawn_vehicle(self.last_spawn_time):
            if len(self.vehicles) < self.scenario.nb_vehicules:
                direction = random.choice(["EST", "OUEST", "NORD", "SUD"])
                vehicle = Vehicle(direction, self.db_manager)
                vehicle.distance_securite = self.scenario.distance_securite
                self.vehicles.append(vehicle)
                self.last_spawn_time = time.time()
        
        # Mise à jour du feu
        self.traffic_light.update(self.scenario.durees_feu, self.scenario.name)
        
        # Vérification des collisions
        self.logger.check_collisions(self.vehicles)
        self.collisions = self.logger.collision_count
        
        # Mise à jour des véhicules
        for v in self.vehicles:
            # D'ABORD : vérifier s'il y a un véhicule devant (PRIORITÉ 1)
            vehicle_ahead = v.check_vehicle_ahead(self.vehicles)
            
            if vehicle_ahead:
                # Il y a quelqu'un devant : s'arrêter ou ralentir
                if vehicle_ahead.is_stopped or vehicle_ahead.speed_value < 0.5:
                    v.stop()
                else:
                    v.slow_down()
            else:
                # Pas de véhicule devant : regarder LE BON FEU (celui à droite)
                # EST/OUEST regardent les feux EO
                # NORD/SUD regardent les feux NS
                if v.direction in ["EST", "OUEST"]:
                    etat_feu = self.traffic_light.etat_eo
                else:
                    etat_feu = self.traffic_light.etat_ns
                
                self.scenario.apply_behavior(v, etat_feu)
            
            # Déplacer
            v.move()


class Application:
    """Application principale"""
    
    def __init__(self):
        print("=" * 70)
        print("SIMULATION DE CIRCULATION URBAINE - VILLE DE THIÈS")
        print("=" * 70)
        print("\nInitialisation en cours...")
        
        # Base de données
        self.db_manager = DatabaseManager()
        print("✓ Base de données initialisée")
        
        # Scène
        self.scene = TurtleScene()
        print("✓ Scène graphique créée")
        
        # Feu tricolore
        self.traffic_light = TrafficLight(self.db_manager)
        print("✓ Feux tricolores initialisés")
        
        # Scénario initial
        self.scenario = CirculationNormale()
        print("✓ Scénario initial chargé")
        
        # Simulation
        self.simulation = Simulation(self.traffic_light, self.scenario, self.db_manager)
        print("✓ Moteur de simulation créé")
        
        # Interface
        self.gui = GUI(self.simulation, self.scene.screen)
        print("✓ Interface de contrôle prête")
        
        # Vues des feux (4 feux : 1 par direction) - HORS DE LA ROUTE
        # Chaque feu est positionné sur le côté DROIT de la voie qu'il contrôle
        self.traffic_light_views = {
            'EST': TrafficLightView(-70, -100, "NS"),    # Feu pour EST (côté SUD-gauche)
            'OUEST': TrafficLightView(70, 100, "NS"),    # Feu pour OUEST (côté NORD-droit)
            'NORD': TrafficLightView(100, -70, "EO"),    # Feu pour NORD (côté EST-bas)
            'SUD': TrafficLightView(-100, 70, "EO"),     # Feu pour SUD (côté OUEST-haut)
        }
        print("✓ Feux tricolores affichés")
        
        # Véhicules initiaux
        self._init_vehicles()
        print("✓ Véhicules initiaux créés")
        
        print("\n" + "=" * 70)
        print("SIMULATION PRÊTE !")
        print("=" * 70)
        self._show_instructions()
        
        # Lancer
        self._main_loop()
    
    def _init_vehicles(self):
        """Crée les véhicules initiaux"""
        directions = ["EST", "OUEST", "NORD", "SUD"]
        for i in range(self.scenario.nb_vehicules):
            direction = directions[i % len(directions)]
            vehicle = Vehicle(direction, self.db_manager)
            vehicle.distance_securite = self.scenario.distance_securite
            self.simulation.vehicles.append(vehicle)
    
    def _main_loop(self):
        """Boucle principale de la simulation"""
        try:
            while True:
                # Mise à jour
                self.simulation.update()
                
                # Affichage des feux
                for direction in ['EST', 'OUEST', 'NORD', 'SUD']:
                    if direction in ['EST', 'OUEST']:
                        etat = self.traffic_light.etat_eo
                    else:
                        etat = self.traffic_light.etat_ns
                    
                    self.traffic_light_views[direction].draw(etat, self.traffic_light.clignotement)
                
                # Mise à jour du statut
                self.gui.update_status()
                
                # Rafraîchir
                self.scene.refresh()
                
                time.sleep(0.03)
        
        except turtle.Terminator:
            print("\nSimulation terminée.")
        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur.")
        finally:
            print("Fermeture de l'application...")
    
    def _show_instructions(self):
        """Affiche les instructions"""
        print("\n📖 INSTRUCTIONS:")
        print("   • START  : Démarre la simulation")
        print("   • PAUSE  : Met en pause / reprend")
        print("   • STOP   : Arrête complètement")
        print("   • RESET  : Réinitialise tout")
        print("   • NORMALE: Scénario de trafic normal")
        print("   • POINTE : Scénario d'heure de pointe")
        print("   • NUIT   : Scénario de mode nuit")
        print("   • MANUEL : Change manuellement les feux\n")


def main():
    """Point d'entrée du programme"""
    try:
        app = Application()
        turtle.mainloop()
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nMerci d'avoir utilisé la simulation de trafic !")
        print("Université Iba Der Thiam de Thiès - L3 Informatique\n")


if __name__ == "__main__":
    main()
