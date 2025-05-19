"""
A script to run a game between two human players,
using the GUI.

Run (from root directory) with:

python -m scripts.human_vs_human
"""

from src.codenames import Game
from src.codenames_types import Player, Role
from src.board_gui import BoardGUI


def main():
    game = Game()
    game.setup_game()

    game.add_player(Player(Role.SPYMASTER))
    game.add_player(Player(Role.OPERATIVE))

    gui = BoardGUI(game)
    gui.run()


if __name__ == "__main__":
    main()
