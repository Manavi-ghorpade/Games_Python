"""
Contains a basic UI implementation for codenames.

NOTE: You can treat this file as a black box - you do not need to understand or modify it.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.codenames import Game
from src.codenames_types import Card, Player, Role
from src.algorithmic_player import AlgorithmicPlayer


class BoardGUI:
    def __init__(self, game: Game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Codenames")
        self.root.geometry("800x600")

        # Set default button background for macOS
        self.root.option_add("*Button.Background", "white")
        self.root.option_add("*Button.activeBackground", "white")

        # Initialize AI timer id
        self.ai_timer_id = None

        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create board frame
        self.board_frame = ttk.Frame(self.main_frame)
        self.board_frame.grid(row=0, column=0, columnspan=2, pady=10)

        # Create status frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Create control frame
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Initialize board buttons
        self.card_buttons = []
        self.create_board()

        # Initialize status label
        self.status_label = ttk.Label(self.status_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=0, column=0, pady=5)

        # Add current clue label
        self.clue_display_label = ttk.Label(
            self.status_frame, text="", font=("Arial", 11)
        )
        self.clue_display_label.grid(row=1, column=0, pady=3)

        # Add spymaster legend label (initially hidden)
        self.spymaster_legend = ttk.Label(
            self.status_frame, text="✓ = Revealed cards", font=("Arial", 10)
        )
        self.spymaster_legend.grid(row=2, column=0, pady=2)

        # Add AI action label
        self.ai_action_label = ttk.Label(self.status_frame, text="", font=("Arial", 10))
        self.ai_action_label.grid(row=3, column=0, pady=2)

        # Initialize control buttons
        self.create_controls()

        # Update the display
        self.update_display()

        # Schedule AI turn if needed
        self.schedule_ai_turn()

    def get_color(self, card: Card, is_spymaster: bool) -> str:
        """Determine the color to display for a card based on its type and reveal status."""

        # First check if we should show the color (card is revealed or viewer is spymaster)
        if card.revealed or is_spymaster:
            # Compare card type value for more reliable comparison
            card_type_value = card.card_type.value

            # For spymasters, use slightly different colors for revealed cards
            if card.revealed and is_spymaster:
                if card_type_value == "red":
                    return "#ffb3b3"  # Lighter red for revealed cards
                elif card_type_value == "blue":
                    return "#b3ccff"  # Lighter blue for revealed cards
                elif card_type_value == "neutral":
                    return "#f9f9f9"  # Almost white for revealed neutrals
                elif card_type_value == "assassin":
                    return "#666666"  # Lighter gray for revealed assassin
            else:
                if card_type_value == "red":
                    return "#ff6666"  # Brighter red (more visible on macOS)
                elif card_type_value == "blue":
                    return "#6699ff"  # Brighter blue (more visible on macOS)
                elif card_type_value == "neutral":
                    return "#e6e6e6"  # Slightly darker gray (more visible on macOS)
                elif card_type_value == "assassin":
                    return "#333333"  # Dark gray (macOS doesn't handle pure black well)

            # Fallback for unknown card types
            return "#ffffff"

        # Default: white for unrevealed cards that shouldn't show color
        return "#ffffff"

    def create_board(self):
        for i in range(5):
            for j in range(5):
                index = i * 5 + j
                btn = tk.Button(
                    self.board_frame,
                    width=12,
                    height=4,
                    font=("Arial", 10, "bold"),
                    borderwidth=1,
                    relief="solid",
                    padx=10,
                    pady=10,
                    command=lambda idx=index: self.on_card_click(idx),
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.card_buttons.append(btn)

    def create_controls(self):
        # Clue entry
        self.clue_var = tk.StringVar()
        self.number_var = tk.StringVar()

        ttk.Label(self.control_frame, text="Clue:").grid(row=0, column=0, padx=5)
        self.clue_entry = ttk.Entry(self.control_frame, textvariable=self.clue_var)
        self.clue_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.control_frame, text="Number:").grid(row=0, column=2, padx=5)
        self.number_entry = ttk.Entry(
            self.control_frame, textvariable=self.number_var, width=5
        )
        self.number_entry.grid(row=0, column=3, padx=5)

        # Action buttons
        self.give_clue_btn = ttk.Button(
            self.control_frame, text="Give Clue", command=self.on_give_clue
        )
        self.give_clue_btn.grid(row=0, column=4, padx=5)

        self.pass_btn = ttk.Button(
            self.control_frame, text="Pass Turn", command=self.on_pass_turn
        )
        self.pass_btn.grid(row=0, column=5, padx=5)

        # AI player control
        # self.toggle_ai_btn = ttk.Button(self.control_frame, text="Toggle AI Turn", command=self.on_toggle_ai)
        # self.toggle_ai_btn.grid(row=0, column=6, padx=5)

    def update_display(self):
        current_player = self.game.get_current_player()
        is_spymaster = current_player.is_spymaster

        # Check if the current player is an algorithmic player
        is_ai = isinstance(current_player, AlgorithmicPlayer)

        # Update status
        status_text = "Current player: "
        status_text += "Spymaster" if is_spymaster else "Operative"
        if is_ai:
            status_text += " (AI)"
        self.status_label.config(text=status_text)

        # Update current clue display
        if self.game.current_clue and not is_spymaster:
            self.clue_display_label.config(
                text=f"Current clue: {self.game.current_clue} ({self.game.current_count})",
                foreground="red",
            )
            self.clue_display_label.grid(row=1, column=0, pady=3)
        else:
            self.clue_display_label.grid_remove()

        # Show or hide spymaster legend based on current role
        if is_spymaster:
            self.spymaster_legend.grid(row=2, column=0, pady=2)
        else:
            self.spymaster_legend.grid_remove()

        # Update board
        for i, (card, btn) in enumerate(zip(self.game.board, self.card_buttons)):
            # Get color based on the current player's role
            color = self.get_color(card, is_spymaster)

            # Text formatting for revealed cards for spymasters
            font_style = "Arial"
            font_weight = "bold"
            font_size = 10

            # Set default text (the card word)
            display_text = card.word

            # For spymasters, show revealed cards with a different style
            if is_spymaster and card.revealed:
                # Add a checkmark to indicate that it's revealed
                display_text = f"✓ {card.word}"
                # Use a darker text color for revealed cards to show they're already played
                text_color = "#666666"
            else:
                text_color = "black"

            # Configure for macOS compatibility
            btn.configure(
                text=display_text,
                fg=text_color,
                disabledforeground=text_color,
                bg=color,
                activebackground=color,
                highlightbackground=color,
                highlightcolor=color,
                relief="solid" if not card.revealed else "sunken",
                font=(font_style, font_size, font_weight),
                state="normal",
            )

            # Add border for revealed cards when viewed by spymaster
            if is_spymaster and card.revealed:
                btn.configure(borderwidth=3)
            else:
                btn.configure(borderwidth=1)

            # Handle button state differently for spymasters and operatives
            if is_spymaster or is_ai:
                # Spymasters and AI players can't be directly controlled
                btn.config(state="disabled")
            else:
                # Operatives can only click unrevealed cards
                btn.config(state="normal" if not card.revealed else "disabled")

        # Update control buttons
        if is_spymaster and not is_ai:
            self.clue_entry.config(state="normal")
            self.number_entry.config(state="normal")
            self.give_clue_btn.config(state="normal")
        else:
            self.clue_entry.config(state="disabled")
            self.number_entry.config(state="disabled")
            self.give_clue_btn.config(state="disabled")

        # Human players can pass; AI players are controlled automatically
        self.pass_btn.config(state="normal" if not is_ai else "disabled")

        # Schedule AI turn if the current player is an algorithmic player
        self.schedule_ai_turn()

        # Check for game over
        if self.game.game_over:
            if self.game.winner:
                messagebox.showinfo(
                    "Game Over", "Success! You found all the red cards!"
                )
            else:
                messagebox.showinfo("Game Over", "Game Over! You hit the assassin!")
            self.root.quit()

    def on_card_click(self, index):
        current_player = self.game.get_current_player()

        # Spymasters can't click cards
        if current_player.is_spymaster:
            return

        # AI players can't be controlled manually
        if isinstance(current_player, AlgorithmicPlayer):
            return

        # Get the card and check if it's already revealed
        card = self.game.board[index]
        if card.revealed:
            return

        # Reveal the card in the game model
        self.game.handle_reveal_card(card.word)
        self.update_display()

    def on_give_clue(self):
        current_player = self.game.get_current_player()
        if current_player.is_spymaster and not isinstance(
            current_player, AlgorithmicPlayer
        ):
            clue = self.clue_var.get().strip()
            try:
                number = int(self.number_var.get())
                if clue and 0 <= number <= 25:
                    # Set the clue in the game
                    self.game.handle_give_clue(clue, number)
                    self.clue_var.set("")
                    self.number_var.set("")
                    self.update_display()
                else:
                    messagebox.showerror(
                        "Error", "Please enter a valid clue and number"
                    )
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

    def on_pass_turn(self):
        current_player = self.game.get_current_player()
        # Only human players can pass manually
        if not isinstance(current_player, AlgorithmicPlayer):
            self.game.handle_reveal_card(None)
            self.update_display()

    def execute_ai_turn(self):
        """Execute a turn for an AI player."""
        self.ai_timer_id = None  # Clear the timer ID as we're executing now
        current_player = self.game.get_current_player()
        if not isinstance(current_player, AlgorithmicPlayer):
            return False  # Not an AI player

        # Get the AI's action
        if current_player.is_spymaster:
            clue, count = current_player.get_spymaster_action(self.game)
            self.ai_action_label.config(
                text=f"AI Spymaster gives clue: '{clue}' ({count})",
                foreground="blue",
            )
            self.game.handle_give_clue(clue, count)
        else:
            word = current_player.get_operative_action(self.game)
            if word is None:
                self.ai_action_label.config(
                    text="AI Operative passes turn", foreground="orange"
                )
            else:
                self.ai_action_label.config(
                    text=f"AI Operative selects card: '{word}'",
                    foreground="green",
                )
            self.game.handle_reveal_card(word)

        self.ai_action_label.grid(row=3, column=0, pady=2)

        self.update_display()
        return False

    def schedule_ai_turn(self):
        """Schedule an AI turn if the current player is an algorithmic player."""
        # Cancel any existing timer
        if self.ai_timer_id:
            self.root.after_cancel(self.ai_timer_id)
            self.ai_timer_id = None

        current_player = self.game.get_current_player()
        if isinstance(current_player, AlgorithmicPlayer) and not self.game.game_over:
            # Schedule the AI turn after a short delay (1 second)
            self.ai_timer_id = self.root.after(1000, self.execute_ai_turn)

    def on_toggle_ai(self):
        """Toggle the current player between human and AI."""
        current_player = self.game.get_current_player()
        index = self.game.current_player_index

        # If the current player is human, replace with AI
        if not isinstance(current_player, AlgorithmicPlayer):
            role = Role.SPYMASTER if current_player.is_spymaster else Role.OPERATIVE
            # Replace the player in the game's player list
            self.game.players[index] = AlgorithmicPlayer(role)
            messagebox.showinfo("AI Player", f"Switched to AI {role.name}")
        else:
            # If the current player is AI, replace with human
            role = Role.SPYMASTER if current_player.is_spymaster else Role.OPERATIVE
            # Replace the AI with a human player
            self.game.players[index] = Player(role)
            messagebox.showinfo("Human Player", f"Switched to human {role.name}")

        # Update the display
        self.update_display()

    def run(self):
        self.root.mainloop()
