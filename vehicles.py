"""
Module de gestion des véhicules
Définit le comportement et l'animation des véhicules
"""

import turtle
import random
import math


class Vehicle(turtle.Turtle):
    """Classe représentant un véhicule dans la simulation"""
    
    _id_counter = 0
    _car_shapes_registered = False
    
    @classmethod
    def _register_car_shapes(cls):
        """Enregistre les formes de voitures personnalisées une seule fois"""
        if cls._car_shapes_registered:
            return
        
        screen = turtle.Screen()
        
        # Forme de voiture réaliste (vue de dessus)
        car_shape = (
            # Avant de la voiture
            (-10, -6), (-10, -8), (-8, -10), (8, -10), (10, -8), (10, -6),
            # Côté droit avec rétroviseur
            (10, -4), (12, -4), (12, 0), (10, 0),
            # Arrière droit
            (10, 6), (10, 8), (8, 10), 
            # Arrière
            (-8, 10), (-10, 8), (-10, 6),
            # Côté gauche avec rétroviseur
            (-10, 0), (-12, 0), (-12, -4), (-10, -4),
            # Fermeture
            (-10, -6)
        )
        
        screen.register_shape("car_shape", car_shape)
        cls._car_shapes_registered = True
    
    def __init__(self, direction="EST", db_manager=None):
        super().__init__()
        Vehicle._id_counter += 1
        self.id = Vehicle._id_counter
        self.direction = direction
        self.db_manager = db_manager
        
        # Enregistrer les formes de voitures
        Vehicle._register_car_shapes()
        
        # Configuration graphique - VOITURE RÉALISTE
        self.shape("car_shape")
        self.shapesize(1.5)
        self.color(random.choice([
            "#E74C3C",  # Rouge vif
            "#3498DB",  # Bleu
            "#2ECC71",  # Vert
            "#F39C12",  # Orange
            "#9B59B6",  # Violet
            "#1ABC9C",  # Turquoise
            "#34495E",  # Gris foncé
            "#E67E22"   # Orange foncé
        ]))
        self.penup()
        
        # Vitesse et état
        self.speed_value = 2
        self.max_speed = 2
        self.is_stopped = False
        self.distance_securite = 40
        self.crossed_intersection = False
        
        self._set_start_position()
        
        # Journalisation
        if self.db_manager:
            self.db_manager.log_event('VOITURE', 'Création véhicule',
                                     id_voiture=self.id,
                                     position_x=self.xcor(),
                                     position_y=self.ycor(),
                                     vitesse=self.speed_value)
    
    def _set_start_position(self):
        """Positionne le véhicule à sa position de départ selon le schéma du carrefour"""
        if self.direction == "EST":
            self.goto(-420, -20)  # Voie basse (en dessous de la ligne centrale)
            self.setheading(0)
        elif self.direction == "OUEST":
            self.goto(420, 20)    # Voie haute (au-dessus de la ligne centrale)
            self.setheading(180)
        elif self.direction == "NORD":
            self.goto(20, -300)   # Voie de droite pour MONTER (x > 0)
            self.setheading(90)
        elif self.direction == "SUD":
            self.goto(-20, 300)   # Voie de gauche pour DESCENDRE (x < 0)
            self.setheading(270)
    
    def move(self):
        """Déplace le véhicule"""
        if not self.is_stopped:
            self.forward(self.speed_value)
        
        # Réinitialisation si sort de l'écran
        if abs(self.xcor()) > 450 or abs(self.ycor()) > 450:
            self._set_start_position()
            if self.db_manager:
                self.db_manager.log_event('VOITURE', 'Réapparition véhicule',
                                         id_voiture=self.id,
                                         position_x=self.xcor(),
                                         position_y=self.ycor())
    
    def stop(self):
        """Arrête le véhicule"""
        if not self.is_stopped:
            self.is_stopped = True
            self.speed_value = 0
            if self.db_manager:
                self.db_manager.log_event('VOITURE', 'Arrêt au feu rouge',
                                         id_voiture=self.id,
                                         etat_feu='ROUGE',
                                         position_x=self.xcor(),
                                         position_y=self.ycor(),
                                         vitesse=0.0)
    
    def move_forward(self):
        """Redémarre le véhicule"""
        if self.is_stopped:
            self.is_stopped = False
            if self.db_manager:
                self.db_manager.log_event('VOITURE', 'Redémarrage au feu vert',
                                         id_voiture=self.id,
                                         position_x=self.xcor(),
                                         position_y=self.ycor())
        self.speed_value = self.max_speed
    
    def slow_down(self):
        """Ralentit le véhicule progressivement"""
        if self.is_stopped:
            self.is_stopped = False
            self.speed_value = self.max_speed * 0.3
        else:
            self.speed_value = max(0.3, self.max_speed * 0.4)
    
    def check_vehicle_ahead(self, vehicles):
        """Vérifie si un véhicule est trop près devant - EMPÊCHE LES DÉPASSEMENTS"""
        closest = None
        min_distance = float('inf')
        
        for other in vehicles:
            if other.id == self.id or other.direction != self.direction:
                continue
            
            if self._is_behind(other):
                distance = math.sqrt((self.xcor() - other.xcor())**2 + 
                                   (self.ycor() - other.ycor())**2)
                
                # Garder le plus proche devant
                if distance < min_distance:
                    min_distance = distance
                    closest = other
        
        # Si quelqu'un est trop près, s'arrêter immédiatement
        if closest and min_distance < 50:
            return closest
        
        return None
    
    def _is_behind(self, other_vehicle):
        """Vérifie si ce véhicule est derrière un autre"""
        if self.direction == "EST":
            return self.xcor() < other_vehicle.xcor()
        elif self.direction == "OUEST":
            return self.xcor() > other_vehicle.xcor()
        elif self.direction == "NORD":
            return self.ycor() < other_vehicle.ycor()
        elif self.direction == "SUD":
            return self.ycor() > other_vehicle.ycor()
        return False
