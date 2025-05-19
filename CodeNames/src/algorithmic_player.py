"""
An example implementation of a Codenames strategy.

In the second part, you will need to modify this file to implement your own strategy.
"""

import random
from src.helpers import get_english_words
from src.codenames_types import Player, Role, CardType


class AlgorithmicPlayer(Player):

    def __init__(self, role: Role = Role.OPERATIVE):
        super().__init__(role)

    def get_spymaster_action(self, game) -> tuple[str, int]:
        """
        Generate a clue as the spymaster.

        Valid clue words are any words in the english language,
        that are not one of the cards on the board.
        """
        # TODO: Remove and replace with your own algorithm
        red_cards = [
            card
            for card in game.board
            if card.card_type == CardType.RED and not card.revealed
        ]

        if not red_cards:
            return None

        clue = random.choice(get_english_words())
        return clue, random.randint(1, 3)

    def get_operative_action(self, game) -> int | None:
        """

        Select a card or pass as the operative (guesser).

        Currently selects a random card from the board.
        """

        # TODO: Remove and replace with your own algorithm
        current_clue = game.current_clue
        current_count = game.current_count

        unrevealed_cards = [card for card in game.board if not card.revealed]

        if not unrevealed_cards:
            return None

        selected_card = random.choice(unrevealed_cards)

        return selected_card.word
