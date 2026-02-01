"""
Module de journalisation
Gère les logs et événements de la simulation
"""

import time
import math
import turtle


class Logger:
    """Gère la journalisation et les alertes visuelles"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.collision_count = 0
        self.violation_count = 0
        self.last_warning_time = 0
    
    def log_collision(self, v1, v2, distance):
        """Journalise une collision"""
        self.collision_count += 1
        
        self.db_manager.log_event(
            'COLLISION',
            'Collision détectée',
            id_voiture=v1.id,
            position_x=(v1.xcor() + v2.xcor()) / 2,
            position_y=(v1.ycor() + v2.ycor()) / 2,
            vitesse=0.0
        )
        
        self._show_collision_warning(v1, v2)
    
    def log_violation(self, v1, v2, distance, recommended):
        """Journalise une violation de distance"""
        self.violation_count += 1
        
        self.db_manager.log_event(
            'VIOLATION',
            'Distance de sécurité violée',
            id_voiture=v1.id,
            position_x=v1.xcor(),
            position_y=v1.ycor()
        )
        
        now = time.time()
        if now - self.last_warning_time > 2:
            self._show_violation_warning(v1, v2, distance)
            self.last_warning_time = now
    
    def _show_collision_warning(self, v1, v2):
        """Affiche un avertissement de collision"""
        warning = turtle.Turtle()
        warning.hideturtle()
        warning.penup()
        warning.goto(0, 280)
        warning.color("red")
        warning.write("⚠ COLLISION DÉTECTÉE !", 
                     align="center", font=("Arial", 14, "bold"))
        turtle.ontimer(lambda: warning.clear(), 2000)
    
    def _show_violation_warning(self, v1, v2, distance):
        """Affiche un avertissement de violation"""
        warning = turtle.Turtle()
        warning.hideturtle()
        warning.penup()
        warning.goto(0, 300)
        warning.color("orange")
        warning.write(f"⚠ Distance de sécurité: {distance:.1f} pixels", 
                     align="center", font=("Arial", 10, "bold"))
        turtle.ontimer(lambda: warning.clear(), 1000)
    
    def check_collisions(self, vehicles, distance_threshold=18):
        """Vérifie les collisions entre véhicules"""
        for i, v1 in enumerate(vehicles):
            for j, v2 in enumerate(vehicles):
                if i >= j:
                    continue
                
                distance = math.sqrt((v1.xcor() - v2.xcor())**2 + 
                                   (v1.ycor() - v2.ycor())**2)
                
                # Collision SEULEMENT si:
                # 1. Sur la même voie (même direction)
                # 2. Ou dans le carrefour ET véhicules différents
                same_direction = (v1.direction == v2.direction)
                in_intersection = (abs(v1.xcor()) < 70 and abs(v1.ycor()) < 70 and 
                                 abs(v2.xcor()) < 70 and abs(v2.ycor()) < 70)
                
                if distance < distance_threshold and (same_direction or in_intersection):
                    self.log_collision(v1, v2, distance)
                    v1.stop()
                    v2.stop()
