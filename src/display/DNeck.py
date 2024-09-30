__author__ = "Eliot Christon"
__email__  = "eliot.christon@gmail.com"
__github__ = "eliot-christon"

"""
DNeck.py
~~~~~~~~

This module contains the main class for the display of the interface when the instrument is a neck instrument.
"""

from typing import Tuple, Dict, List
import pygame

from ..instrument.INeck import INeck


class DNeck:
    """
    Display class for neck instruments.
    """

    def __init__(self, instrument:INeck):
        self.instrument = instrument

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
        }

        self.font = pygame.font.Font(None, 36)

    def run(self):
        """
        Main loop of the display.
        """
        while self.running:
            self.screen.fill(self.colors["white"])
            self.draw_neck()
            self.draw_position()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_neck(self):
        """
        Draws the neck of the instrument.
        the neck should occupy all the screen 
        """