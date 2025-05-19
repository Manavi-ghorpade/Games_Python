"""
Contains the main implementation of the logic of Codenames.

You will need to make changes to this file.
"""

from typing import List, Optional
import random

# Import common classes from the common module
from src.codenames_types import CardType, Card, Player


class Game:
    def __init__(self):
        # The ~425 words that can be on a codenames board
        self.available_words = self._load_words()

        self.board: List[Card] = []

        self.players: List[Player] = []
        self.current_player_index: int = 0

        self.current_clue: Optional[str] = None
        self.current_count: Optional[int] = None

        # True if won, False if lost, None if unfinished
        self.winner: Optional[bool] = None

        self.consecutive_guesses: int = 0
        self.revealed_red_cards_count:int = 0 #count how many red guessed

    def _load_words(self) -> List[str]:
        with open("data/codenames_words.txt", "r") as f:
            return [line.strip() for line in f.readlines()]

    def setup_game(self):
        # TODO: Create the board with 25 cards - 9 red, 0 blue, 15 neutral, 1 assassin)
        words = random.sample(self.available_words, 25) #give list of 25 cards
        #25 - start 0 - go till 24
        idx_list = list(range(25)) 
        #print(idx_list)
        # 0 , 3, 4 , 6 ,10, .....
        #
        for idx in idx_list[:9]:  #shpuld be just 9 for red
            self.board.append(Card(words[idx],CardType.RED))
        for idx in idx_list[9:9+15]: # 15 neutrals 
            self.board.append(Card(words[idx],CardType.NEUTRAL))
        self.board.append(Card(words[9+15], CardType.ASSASSIN)) # 1 card assassin
        random.shuffle(self.board)
        pass

    def add_player(self, player: Player) -> None:
        """Add an existing Player object to the game."""
        self.players.append(player)

    def get_current_player(self) -> Player:
        """Get the player who's turn it is."""
        return self.players[self.current_player_index]

    def handle_give_clue(self, clue: str, count: int) -> None:
        """
        Called when a spymaster gives a clue to their team and updates the
        internal state of the game to reflect the action.
        """
        print(f"Spymaster gave clue: {clue} ({count})")
        self.current_clue = clue
        self.current_count = count
        self._next_turn()

    def handle_reveal_card(self, word: str | None) -> None:
        """
        Called when an operative reveals a card - which can either be
        a red card, a neutral card, or an assassin card.
        The input is either the word guessed, or None if the player passed.
        The function should update the internal state of the game to reflect the
        action taken.
        """
        if word is None:
            self._next_turn()
            return

        for card in self.board:
            if card.word.lower() == word.lower() and not card.revealed:
                # TODO: Handle when the operative reveals a card
                color_of_card = card.card_type #color of current card
                card.revealed = True #mark as viewed
                if(color_of_card == CardType.RED):  #if match
                    self.revealed_red_cards_count+=1 #track number of red cards revealed
                    self.consecutive_guesses += 1
                    if(self.consecutive_guesses >= self.current_count+1):
                        #change turn
                        self.consecutive_guesses = 0
                        self._next_turn()
                        break
                    else:
                        pass #keep on guessing
                elif(color_of_card == CardType.NEUTRAL):  #wrong guess
                    self.consecutive_guesses = 0
                    self._next_turn()
                    break
                elif(color_of_card == CardType.ASSASSIN): #end game if assassin
                    self.winner = False
                    break
        if self.revealed_red_cards_count == 9: #if clicked all red cards it is win
            self.winner = True

    @property
    def game_over(self) -> bool:
        return self.winner is not None

    def _next_turn(self) -> None:
        """
        Helper method to advance the game to the next turn - you should
        use this in the implementation of the above methods.
        """
        #0+1%2=1, 1+1%2=0 , 0->1->0....
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        # Clear clue when it's the spymaster's turn
        if self.get_current_player().is_spymaster:
            self.current_clue = None
            self.current_count = None