"""
15-Puzzle Game Entry Point
--------------------------
This script initializes the GUI for the 15-puzzle game and starts the application.
"""

import logging
import tkinter as tk
from src.ui.game_interface import GameInterface

logging.basicConfig(level=logging.INFO)

def main():
    """Main function to start the game."""
    root = tk.Tk()
    game = GameInterface(root)
    game.run()

if __name__ == "__main__":
    main()
