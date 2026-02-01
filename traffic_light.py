"""
Module de gestion du feu tricolore
Gère les états et les transitions du feu tricolore
"""

from enum import Enum
import time


class EtatFeu(Enum):
    """États possibles du feu tricolore"""
    ROUGE = "ROUGE"
    ORANGE = "ORANGE"
    VERT = "VERT"
    ORANGE_CLIGNOTANT = "ORANGE_CLIGNOTANT"


class TrafficLight:
    """Classe représentant un feu tricolore"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.etat_ns = EtatFeu.ROUGE  # Nord-Sud
        self.etat_eo = EtatFeu.VERT   # Est-Ouest
        self.phase = "EO"  # Phase active
        self.last_change = time.time()
        self.mode_manuel = False
        self.clignotement = True
        self.last_blink = time.time()
        
        # Journalisation initialisation
        self.db_manager.log_event('SYSTEME', 'Initialisation feu tricolore',
                                  etat_feu=f'NS:{self.etat_ns.value}, EO:{self.etat_eo.value}')
    
    def update(self, durees, scenario_name):
        """Met à jour l'état du feu selon le scénario"""
        now = time.time()
        
        # Mode nuit : orange clignotant
        if scenario_name == "Mode nuit":
            if now - self.last_blink > 0.5:
                self.clignotement = not self.clignotement
                self.last_blink = now
            self.etat_ns = EtatFeu.ORANGE_CLIGNOTANT
            self.etat_eo = EtatFeu.ORANGE_CLIGNOTANT
            return
        
        # Ne pas changer en mode manuel
        if self.mode_manuel:
            return
        
        # Gestion automatique des phases
        if self.phase == "EO":
            if self.etat_eo == EtatFeu.VERT and now - self.last_change > durees.get(EtatFeu.VERT, 5):
                self._next_eo()
            elif self.etat_eo == EtatFeu.ORANGE and now - self.last_change > durees.get(EtatFeu.ORANGE, 2):
                self._next_eo()
            elif self.etat_eo == EtatFeu.ROUGE and now - self.last_change > 1:
                self.phase = "NS"
                self.etat_ns = EtatFeu.VERT
                self.db_manager.log_event('FEU', 'Passage NS à VERT', etat_feu='NS:VERT')
                self.last_change = time.time()
        else:
            if self.etat_ns == EtatFeu.VERT and now - self.last_change > durees.get(EtatFeu.VERT, 5):
                self._next_ns()
            elif self.etat_ns == EtatFeu.ORANGE and now - self.last_change > durees.get(EtatFeu.ORANGE, 2):
                self._next_ns()
            elif self.etat_ns == EtatFeu.ROUGE and now - self.last_change > 1:
                self.phase = "EO"
                self.etat_eo = EtatFeu.VERT
                self.db_manager.log_event('FEU', 'Passage EO à VERT', etat_feu='EO:VERT')
                self.last_change = time.time()
    
    def _next_eo(self):
        """Passe à l'état suivant pour Est-Ouest"""
        if self.etat_eo == EtatFeu.VERT:
            self.etat_eo = EtatFeu.ORANGE
            self.db_manager.log_event('FEU', 'EO passe à ORANGE', etat_feu='EO:ORANGE')
        elif self.etat_eo == EtatFeu.ORANGE:
            self.etat_eo = EtatFeu.ROUGE
            # L'autre axe reste ROUGE pendant 1 seconde avant de passer au VERT
            self.db_manager.log_event('FEU', 'EO passe à ROUGE', etat_feu='EO:ROUGE')
        self.last_change = time.time()
    
    def _next_ns(self):
        """Passe à l'état suivant pour Nord-Sud"""
        if self.etat_ns == EtatFeu.VERT:
            self.etat_ns = EtatFeu.ORANGE
            self.db_manager.log_event('FEU', 'NS passe à ORANGE', etat_feu='NS:ORANGE')
        elif self.etat_ns == EtatFeu.ORANGE:
            self.etat_ns = EtatFeu.ROUGE
            # L'autre axe reste ROUGE pendant 1 seconde avant de passer au VERT
            self.db_manager.log_event('FEU', 'NS passe à ROUGE', etat_feu='NS:ROUGE')
        self.last_change = time.time()
    
    def manual_change(self):
        """Change manuellement l'état du feu"""
        self.mode_manuel = True
        
        if self.phase == "EO":
            self.phase = "NS"
            self.etat_eo = EtatFeu.ROUGE
            self.etat_ns = EtatFeu.VERT
        else:
            self.phase = "EO"
            self.etat_ns = EtatFeu.ROUGE
            self.etat_eo = EtatFeu.VERT
        
        self.db_manager.log_event('FEU', 'Changement manuel', 
                                  etat_feu=f'NS:{self.etat_ns.value}, EO:{self.etat_eo.value}')
        self.last_change = time.time()
    
    def set_auto_mode(self):
        """Active le mode automatique"""
        self.mode_manuel = False
        self.db_manager.log_event('SYSTEME', 'Passage en mode automatique')
