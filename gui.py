"""
Module de l'interface graphique
Gère les boutons de contrôle et l'affichage des informations
"""

import turtle


class Button:
    """Bouton cliquable dans l'interface"""
    
    def __init__(self, x, y, width, height, label, action, color="#3498db"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.color = color
        self.action = action
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.penup()
        self.draw()
    
    def draw(self):
        """Dessine le bouton"""
        self.turtle.clear()
        self.turtle.goto(self.x, self.y)
        self.turtle.color("white", self.color)
        self.turtle.begin_fill()
        for _ in range(2):
            self.turtle.forward(self.width)
            self.turtle.right(90)
            self.turtle.forward(self.height)
            self.turtle.right(90)
        self.turtle.end_fill()
        
        self.turtle.goto(self.x + self.width/2, self.y - self.height/2 - 8)
        self.turtle.color("white")
        self.turtle.write(self.label, align="center", font=("Arial", 11, "bold"))
    
    def is_clicked(self, x, y):
        """Vérifie si le bouton a été cliqué"""
        return (self.x <= x <= self.x + self.width and 
                self.y - self.height <= y <= self.y)
    
    def click(self):
        """Exécute l'action du bouton"""
        self.action()
        self.turtle.color("white", "#2980b9")
        self.draw()
        turtle.ontimer(lambda: self._reset_color(), 100)
    
    def _reset_color(self):
        """Réinitialise la couleur du bouton"""
        self.turtle.color("white", self.color)
        self.draw()


class GUI:
    """Gestion de l'interface graphique complète"""
    
    def __init__(self, simulation, screen):
        self.simulation = simulation
        self.screen = screen
        self.buttons = []
        self.status_turtle = turtle.Turtle()
        self.status_turtle.hideturtle()
        self._draw_sidebar()
        self._create_buttons()
        self.screen.onclick(self._handle_click)
    
    def _draw_sidebar(self):
        """Dessine une belle sidebar à droite"""
        sidebar_drawer = turtle.Turtle()
        sidebar_drawer.hideturtle()
        sidebar_drawer.speed(0)
        sidebar_drawer.penup()
        
        # Fond de la sidebar - BEAUCOUP PLUS À DROITE
        sidebar_drawer.goto(480, 400)
        sidebar_drawer.pendown()
        sidebar_drawer.color("#34495e")
        sidebar_drawer.begin_fill()
        sidebar_drawer.goto(600, 400)
        sidebar_drawer.goto(600, -400)
        sidebar_drawer.goto(480, -400)
        sidebar_drawer.goto(480, 400)
        sidebar_drawer.end_fill()
        
        # Titre ACTIONS
        sidebar_drawer.penup()
        sidebar_drawer.goto(540, 350)
        sidebar_drawer.color("white")
        sidebar_drawer.write("ACTIONS", align="center", font=("Arial", 14, "bold"))
        
        # Ligne séparatrice 1
        sidebar_drawer.goto(490, 330)
        sidebar_drawer.pendown()
        sidebar_drawer.color("#ecf0f1")
        sidebar_drawer.width(2)
        sidebar_drawer.goto(590, 330)
        
        # Titre SCÉNARIOS
        sidebar_drawer.penup()
        sidebar_drawer.goto(540, 60)
        sidebar_drawer.color("white")
        sidebar_drawer.write("SCÉNARIOS", align="center", font=("Arial", 14, "bold"))
        
        # Ligne séparatrice 2
        sidebar_drawer.penup()
        sidebar_drawer.goto(40, 40)
        sidebar_drawer.pendown()
        sidebar_drawer.color("#ecf0f1")
        sidebar_drawer.goto(590, 60)
    
    def _create_buttons(self):
        """Crée tous les boutons dans la sidebar - TRÈS JOLIE"""
        from scenarios import CirculationNormale, HeureDePointe, ModeNuit
        
        # Configuration - BEAUCOUP PLUS À DROITE
        SIDEBAR_X = 490
        BUTTON_WIDTH = 100
        BUTTON_HEIGHT = 40
        VERTICAL_SPACING = 15
        
        # === SECTION ACTIONS ===
        START_Y = 300
        
        self.buttons.append(Button(
            SIDEBAR_X, START_Y, BUTTON_WIDTH, BUTTON_HEIGHT, 
            "▶ START", self.simulation.start, "#27ae60"
        ))
        
        self.buttons.append(Button(
            SIDEBAR_X, START_Y - (BUTTON_HEIGHT + VERTICAL_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT,
            "⏸ PAUSE", self.simulation.pause, "#f39c12"
        ))
        
        self.buttons.append(Button(
            SIDEBAR_X, START_Y - 2*(BUTTON_HEIGHT + VERTICAL_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT,
            "⏹ STOP", self.simulation.stop, "#e74c3c"
        ))
        
        self.buttons.append(Button(
            SIDEBAR_X, START_Y - 3*(BUTTON_HEIGHT + VERTICAL_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT,
            "🔄 Reset", self.simulation.reset, "#3498db"
        ))
        
        # === SECTION SCÉNARIOS ===
        SCENARIOS_START_Y = 30
        
        self.buttons.append(Button(
            SIDEBAR_X, SCENARIOS_START_Y, BUTTON_WIDTH, BUTTON_HEIGHT,
            "🚗 NORMALE", 
            lambda: self.simulation.change_scenario(CirculationNormale()), "#2ecc71"
        ))
        
        self.buttons.append(Button(
            SIDEBAR_X, SCENARIOS_START_Y - (BUTTON_HEIGHT + VERTICAL_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT,
            "🚦 POINTE", 
            lambda: self.simulation.change_scenario(HeureDePointe()), "#e67e22"
        ))
        
        self.buttons.append(Button(
            SIDEBAR_X, SCENARIOS_START_Y - 2*(BUTTON_HEIGHT + VERTICAL_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT,
            "🌙 NUIT", 
            lambda: self.simulation.change_scenario(ModeNuit()), "#8e44ad"
        ))
        
        self.buttons.append(Button(
            SIDEBAR_X, SCENARIOS_START_Y - 3*(BUTTON_HEIGHT + VERTICAL_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT,
            "👆 MANUEL", self.simulation.traffic_light.manual_change, "#9b59b6"
        ))
    
    def _handle_click(self, x, y):
        """Gère les clics de souris"""
        for button in self.buttons:
            if button.is_clicked(x, y):
                button.click()
                break
    
    def update_status(self):
        """Met à jour l'affichage des informations"""
        self.status_turtle.clear()
        self.status_turtle.penup()
        self.status_turtle.color("#2c3e50")
        
        start_x = -480
        start_y = -250
        line_height = 25
        
        def write_line(y, label, value):
            self.status_turtle.goto(start_x, y)
            self.status_turtle.write(label, align="left", font=("Arial", 11, "bold"))
            self.status_turtle.goto(start_x + 120, y)
            self.status_turtle.write(value, align="left", font=("Arial", 11))
        
        # Afficher les informations
        write_line(start_y, "Scénario:", self.simulation.scenario.name)
        
        status = '▶ EN COURS' if self.simulation.running else '⏹ ARRÊTÉ'
        if self.simulation.paused:
            status = '⏸ EN PAUSE'
        write_line(start_y - line_height, "État:", status)
        
        write_line(start_y - 2*line_height, "Véhicules:", str(len(self.simulation.vehicles)))
        
        feux_info = f"NS: {self.simulation.traffic_light.etat_ns.value}"
        feux_info += f" / EO: {self.simulation.traffic_light.etat_eo.value}"
        write_line(start_y - 3*line_height, "Feux:", feux_info)
        
        write_line(start_y - 4*line_height, "Collisions:", str(self.simulation.collisions))
