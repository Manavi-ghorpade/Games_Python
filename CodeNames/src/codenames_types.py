"""
Contains shared types and classes for the Codenames game.
"""

from typing import Dict, Optional, Tuple
from enum import Enum
from abc import ABC


class CardType(Enum):
    RED = "red"
    NEUTRAL = "neutral"
    ASSASSIN = "assassin"


class Role(Enum):
    SPYMASTER = True
    OPERATIVE = False


class Card:
    """
    An instance of a Card on the board
    """

    def __init__(self, word: str, card_type: CardType, revealed: bool = False):
        self.word = word
        self.card_type = card_type
        self.revealed = revealed

    def __str__(self) -> str:
        if self.revealed:
            return f"{self.word} ({self.card_type.value})"
        return self.word


class Player(ABC):
    """
    An instance of a Player playing the game.
    """

    def __init__(self, role: Role = Role.OPERATIVE):
        self.is_spymaster = role == Role.SPYMASTER

    def __str__(self) -> str:
        role = "Spymaster" if self.is_spymaster else "Operative"
        return f"{role}"

    def get_spymaster_action(self, game) -> Tuple[str, int]:
        """
        Child classes should override this to generate a clue: a word and a count.
        """
        return None

    def get_operative_action(self, game) -> str | None:
        """
        Child classes should implement this to select a card from the board.

        Returns: a word from the board, or None if the player chooses to pass.
        """
        return None
