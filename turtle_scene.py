"""
Module de gestion de la scène graphique
Dessine le carrefour, les routes et les feux tricolores
"""

import turtle


class TurtleScene:
    """Gère l'affichage graphique de la simulation"""
    
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(1200, 800)  # Largeur augmentée à 1200
        self.screen.title("Simulation de Circulation Urbaine - Ville de Thiès")
        self.screen.bgcolor("#f0f0f0")
        self.screen.tracer(0)
        
        # Titre - CENTRÉ ET TOUT EN HAUT
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        title_turtle.goto(0, 380)
        title_turtle.color("#2c3e50")
        title_turtle.write("Simulation de Circulation Urbaine - Ville de Thiès", 
                          align="center", font=("Arial", 16, "bold"))
        
        subtitle_turtle = turtle.Turtle()
        subtitle_turtle.hideturtle()
        subtitle_turtle.penup()
        subtitle_turtle.goto(0, 355)
        subtitle_turtle.color("#34495e")
        subtitle_turtle.write("Université Iba Der Thiam de Thiès - L3 Informatique", 
                             align="center", font=("Arial", 11, "italic"))
        
        self.drawer = turtle.Turtle()
        self.drawer.hideturtle()
        self.drawer.speed(0)
        self._draw_intersection()
        self._draw_markings()
    
    def _draw_intersection(self):
        """Dessine le carrefour avec les routes perpendiculaires - CENTRÉ"""
        self.drawer.color("#34495e")
        self.drawer.width(1)
        
        # Route horizontale (EST-OUEST) : de y=-40 à y=+40 (80 pixels de haut)
        # Coin sud-ouest (-450, -40) → coin nord-ouest (-450, +40)
        self.drawer.penup()
        self.drawer.goto(-450, -40)
        self.drawer.pendown()
        self.drawer.begin_fill()
        self.drawer.goto(450, -40)   # Sud-ouest → sud-est
        self.drawer.goto(450, 40)    # Sud-est → nord-est
        self.drawer.goto(-450, 40)   # Nord-est → nord-ouest
        self.drawer.goto(-450, -40)  # Nord-ouest → sud-ouest
        self.drawer.end_fill()
        
        # Route verticale (NORD-SUD) : de x=-40 à x=+40 (80 pixels de large)
        # Coin sud-ouest (-40, -340) → coin sud-est (+40, -340)
        self.drawer.penup()
        self.drawer.goto(-40, -340)
        self.drawer.pendown()
        self.drawer.begin_fill()
        self.drawer.goto(40, -340)   # Sud-ouest → sud-est
        self.drawer.goto(40, 340)    # Sud-est → nord-est
        self.drawer.goto(-40, 340)   # Nord-est → nord-ouest
        self.drawer.goto(-40, -340)  # Nord-ouest → sud-ouest
        self.drawer.end_fill()
    
    def _draw_markings(self):
        """Dessine les marquages au sol (lignes blanches centrales + passages piétons)"""
        self.drawer.color("white")
        self.drawer.width(4)
        self.drawer.penup()
        
        # Ligne pointillée HORIZONTALE (centre de la route horizontale)
        for x in range(-450, 451, 40):
            # Éviter le carrefour central
            if abs(x) > 50:
                self.drawer.goto(x, 0)
                self.drawer.pendown()
                self.drawer.setheading(0)
                self.drawer.forward(20)
                self.drawer.penup()
        
        # Ligne pointillée VERTICALE (centre de la route verticale)  
        for y in range(-340, 341, 40):
            # Éviter le carrefour central
            if abs(y) > 50:
                self.drawer.goto(0, y)
                self.drawer.pendown()
                self.drawer.setheading(90)
                self.drawer.forward(20)
                self.drawer.penup()
        
        # ========== PASSAGES PIÉTONS ==========
        self.drawer.color("white")
        self.drawer.width(3)
        
        # Passage piéton EST (à droite du carrefour)
        for i in range(8):
            self.drawer.penup()
            self.drawer.goto(60 + i*5, -35)
            self.drawer.pendown()
            self.drawer.setheading(90)
            self.drawer.forward(70)
        
        # Passage piéton OUEST (à gauche du carrefour)
        for i in range(8):
            self.drawer.penup()
            self.drawer.goto(-60 - i*5, -35)
            self.drawer.pendown()
            self.drawer.setheading(90)
            self.drawer.forward(70)
        
        # Passage piéton NORD (en haut du carrefour)
        for i in range(8):
            self.drawer.penup()
            self.drawer.goto(-35, 60 + i*5)
            self.drawer.pendown()
            self.drawer.setheading(0)
            self.drawer.forward(70)
        
        # Passage piéton SUD (en bas du carrefour)
        for i in range(8):
            self.drawer.penup()
            self.drawer.goto(-35, -60 - i*5)
            self.drawer.pendown()
            self.drawer.setheading(0)
            self.drawer.forward(70)
    
    def refresh(self):
        """Rafraîchit l'écran"""
        self.screen.update()


class TrafficLightView:
    """Vue graphique d'un feu tricolore"""
    
    def __init__(self, x, y, orientation="NS"):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.width(2)
    
    def draw(self, etat, blink_state=True):
        """Dessine le feu tricolore avec l'état actuel"""
        self.turtle.clear()
        
        # Dessiner le support
        self.turtle.penup()
        
        if self.orientation in ["NORD", "SUD", "NS"]:
            # Feu vertical
            self.turtle.goto(self.x - 15, self.y + 50)
            self.turtle.color("black")
            self.turtle.pendown()
            self.turtle.begin_fill()
            for _ in range(2):
                self.turtle.forward(30)
                self.turtle.right(90)
                self.turtle.forward(100)
                self.turtle.right(90)
            self.turtle.end_fill()
            
            # Dessiner les trois feux
            self._draw_light(self.y + 30, etat.value == "ROUGE", "red")
            self._draw_light(self.y, etat.value == "ORANGE" or (etat.value == "ORANGE_CLIGNOTANT" and blink_state), "orange")
            self._draw_light(self.y - 30, etat.value == "VERT", "green")
        
        else:
            # Feu horizontal
            self.turtle.goto(self.x - 50, self.y + 15)
            self.turtle.color("black")
            self.turtle.pendown()
            self.turtle.begin_fill()
            for _ in range(2):
                self.turtle.forward(100)
                self.turtle.right(90)
                self.turtle.forward(30)
                self.turtle.right(90)
            self.turtle.end_fill()
            
            # Dessiner les trois feux
            self._draw_light_h(self.x - 30, etat.value == "ROUGE", "red")
            self._draw_light_h(self.x, etat.value == "ORANGE" or (etat.value == "ORANGE_CLIGNOTANT" and blink_state), "orange")
            self._draw_light_h(self.x + 30, etat.value == "VERT", "green")
    
    def _draw_light(self, y, active, color):
        """Dessine un feu individuel (vertical)"""
        self.turtle.penup()
        self.turtle.goto(self.x, y)
        if active:
            self.turtle.color(color)
            self.turtle.dot(20)
        else:
            self.turtle.color("#333333")
            self.turtle.dot(20)
    
    def _draw_light_h(self, x, active, color):
        """Dessine un feu individuel (horizontal)"""
        self.turtle.penup()
        self.turtle.goto(x, self.y)
        if active:
            self.turtle.color(color)
            self.turtle.dot(20)
        else:
            self.turtle.color("#333333")
            self.turtle.dot(20)
