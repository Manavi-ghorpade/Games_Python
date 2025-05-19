#!/usr/bin/env python3
"""
Codenames AI vs AI Demo

Run (from root directory) with:

python -m scripts.ai_vs_ai
"""

from src.codenames import Game
from src.codenames_types import Role
from src.algorithmic_player import AlgorithmicPlayer
from src.board_gui import BoardGUI


def main():
    game = Game()
    game.setup_game()

    game.add_player(AlgorithmicPlayer(Role.SPYMASTER))
    game.add_player(AlgorithmicPlayer(Role.OPERATIVE))

    gui = BoardGUI(game)
    gui.run()


if __name__ == "__main__":
    main()
