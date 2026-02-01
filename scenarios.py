"""
Module de gestion des scénarios de circulation
Définit les différents scénarios et leurs paramètres
"""

from traffic_light import EtatFeu
import time


class Scenario:
    """Classe de base abstraite pour les scénarios"""
    
    def __init__(self, name):
        self.name = name
        self.durees_feu = {}
        self.nb_vehicules = 5
        self.taux_apparition = 4.0
        self.distance_securite = 40
    
    def get_duree_feu(self, etat):
        return self.durees_feu.get(etat, 0)
    
    def apply_behavior(self, vehicle, etat_feu):
        """Applique le comportement du véhicule selon le scénario"""
        raise NotImplementedError
    
    def should_spawn_vehicle(self, last_spawn_time):
        """Détermine si un nouveau véhicule doit apparaître"""
        return time.time() - last_spawn_time > self.taux_apparition


class CirculationNormale(Scenario):
    """Scénario 1: Circulation normale"""
    
    def __init__(self):
        super().__init__("Circulation normale")
        self.durees_feu = {
            EtatFeu.ROUGE: 4,
            EtatFeu.VERT: 6,
            EtatFeu.ORANGE: 2
        }
        self.nb_vehicules = 5
        self.taux_apparition = 4.0
        self.distance_securite = 40
    
    def apply_behavior(self, vehicle, etat_feu):
        """Comportement en circulation normale avec respect STRICT des feux"""
        zone_carrefour = 50
        distance_avant_feu = 100
        
        # DÉJÀ dans le carrefour OU APRÈS le carrefour : continuer sans regarder le feu
        if abs(vehicle.xcor()) < zone_carrefour and abs(vehicle.ycor()) < zone_carrefour:
            vehicle.move_forward()
            return
        
        # AVANT le carrefour : respecter le feu UNIQUEMENT si on approche
        if vehicle.direction == "EST":
            # Véhicule vient de l'OUEST (x négatif) et va vers l'EST (x positif)
            if vehicle.xcor() < -distance_avant_feu:
                # Très loin : circuler librement
                vehicle.move_forward()
            elif vehicle.xcor() < -zone_carrefour:
                # Zone d'arrêt AVANT le carrefour : respecter le feu
                if etat_feu == EtatFeu.ROUGE:
                    vehicle.stop()
                elif etat_feu == EtatFeu.ORANGE:
                    if vehicle.xcor() < -80:
                        vehicle.stop()
                    else:
                        vehicle.move_forward()
                else:  # VERT
                    vehicle.move_forward()
            else:
                # APRÈS le feu ou dans le carrefour : toujours avancer
                vehicle.move_forward()
        
        elif vehicle.direction == "OUEST":
            # Véhicule vient de l'EST (x positif) et va vers l'OUEST (x négatif)
            if vehicle.xcor() > distance_avant_feu:
                # Très loin : circuler librement
                vehicle.move_forward()
            elif vehicle.xcor() > zone_carrefour:
                # Zone d'arrêt AVANT le carrefour : respecter le feu
                if etat_feu == EtatFeu.ROUGE:
                    vehicle.stop()
                elif etat_feu == EtatFeu.ORANGE:
                    if vehicle.xcor() > 80:
                        vehicle.stop()
                    else:
                        vehicle.move_forward()
                else:  # VERT
                    vehicle.move_forward()
            else:
                # APRÈS le feu ou dans le carrefour : toujours avancer
                vehicle.move_forward()
        
        elif vehicle.direction == "NORD":
            # Véhicule vient du SUD (y négatif) et va vers le NORD (y positif)
            if vehicle.ycor() < -distance_avant_feu:
                # Très loin : circuler librement
                vehicle.move_forward()
            elif vehicle.ycor() < -zone_carrefour:
                # Zone d'arrêt AVANT le carrefour : respecter le feu
                if etat_feu == EtatFeu.ROUGE:
                    vehicle.stop()
                elif etat_feu == EtatFeu.ORANGE:
                    if vehicle.ycor() < -80:
                        vehicle.stop()
                    else:
                        vehicle.move_forward()
                else:  # VERT
                    vehicle.move_forward()
            else:
                # APRÈS le feu ou dans le carrefour : toujours avancer
                vehicle.move_forward()
        
        elif vehicle.direction == "SUD":
            # Véhicule vient du NORD (y positif) et va vers le SUD (y négatif)
            if vehicle.ycor() > distance_avant_feu:
                # Très loin : circuler librement
                vehicle.move_forward()
            elif vehicle.ycor() > zone_carrefour:
                # Zone d'arrêt AVANT le carrefour : respecter le feu
                if etat_feu == EtatFeu.ROUGE:
                    vehicle.stop()
                elif etat_feu == EtatFeu.ORANGE:
                    if vehicle.ycor() > 80:
                        vehicle.stop()
                    else:
                        vehicle.move_forward()
                else:  # VERT
                    vehicle.move_forward()
            else:
                # APRÈS le feu ou dans le carrefour : toujours avancer
                vehicle.move_forward()


class HeureDePointe(Scenario):
    """Scénario 2: Heure de pointe"""
    
    def __init__(self):
        super().__init__("Heure de pointe")
        self.durees_feu = {
            EtatFeu.ROUGE: 3,
            EtatFeu.VERT: 7,
            EtatFeu.ORANGE: 1
        }
        self.nb_vehicules = 6
        self.taux_apparition = 2.5
        self.distance_securite = 30
    
    def apply_behavior(self, vehicle, etat_feu):
        """Comportement en heure de pointe - démarrage plus rapide"""
        zone_arret = 70
        zone_carrefour = 60
        
        # Dans le carrefour, continuer
        if abs(vehicle.xcor()) < zone_carrefour and abs(vehicle.ycor()) < zone_carrefour:
            vehicle.move_forward()
            return
        
        # Est-Ouest
        if vehicle.direction == "EST":
            if vehicle.xcor() < -zone_arret and etat_feu == EtatFeu.ROUGE:
                vehicle.stop()
            elif vehicle.xcor() < -zone_carrefour and etat_feu == EtatFeu.ORANGE:
                vehicle.slow_down()
            else:
                vehicle.move_forward()
        elif vehicle.direction == "OUEST":
            if vehicle.xcor() > zone_arret and etat_feu == EtatFeu.ROUGE:
                vehicle.stop()
            elif vehicle.xcor() > zone_carrefour and etat_feu == EtatFeu.ORANGE:
                vehicle.slow_down()
            else:
                vehicle.move_forward()
        
        # Nord-Sud
        elif vehicle.direction == "NORD":
            if vehicle.ycor() < -zone_arret and etat_feu == EtatFeu.ROUGE:
                vehicle.stop()
            elif vehicle.ycor() < -zone_carrefour and etat_feu == EtatFeu.ORANGE:
                vehicle.slow_down()
            else:
                vehicle.move_forward()
        elif vehicle.direction == "SUD":
            if vehicle.ycor() > zone_arret and etat_feu == EtatFeu.ROUGE:
                vehicle.stop()
            elif vehicle.ycor() > zone_carrefour and etat_feu == EtatFeu.ORANGE:
                vehicle.slow_down()
            else:
                vehicle.move_forward()


class ModeNuit(Scenario):
    """Scénario 3: Faible circulation (mode nuit)"""
    
    def __init__(self):
        super().__init__("Mode nuit")
        self.durees_feu = {}
        self.nb_vehicules = 3
        self.taux_apparition = 8.0
        self.distance_securite = 60
    
    def apply_behavior(self, vehicle, etat_feu):
        """Comportement en mode nuit - vitesse réduite"""
        vehicle.slow_down()
