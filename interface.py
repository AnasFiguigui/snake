import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Install Pillow if needed: pip install pillow
from UNO_Game import Deck, Hand, single_card_check, win_check

# Helper Functions
def play_card(pos):
    """Handles the player's action to play a card."""
    global top_card
    card = player_hand.single_card(pos)
    if single_card_check(top_card, card):
        player_hand.remove_card(pos + 1)
        update_hand()
        top_card = card  # Update the top card
        update_top_card()  # Refresh the displayed top card
        if win_check(player_hand):
            messagebox.showinfo("UNO", "Player Won!")
            root.quit()
        else:
            pc_turn()  # PC's turn after a valid play
    else:
        messagebox.showerror("UNO", "Invalid Card!")

def pull_card():
    """Handles the player's action to pull a card from the deck."""
    card = deck.deal()
    player_hand.add_card(card)
    update_hand()

def update_hand():
    """Updates the player's hand display in the GUI."""
    for widget in player_frame.winfo_children():
        widget.destroy()
    for idx, card in enumerate(player_hand.cards):
        card_image = ImageTk.PhotoImage(Image.open(card.get_image_path()).resize((100, 150)))
        btn = tk.Button(player_frame, image=card_image, command=lambda idx=idx: play_card(idx))
        btn.image = card_image  # Keep a reference to avoid garbage collection
        btn.pack(side=tk.LEFT)

def update_top_card():
    """Updates the top card image and its name."""
    card_image = ImageTk.PhotoImage(Image.open(top_card.get_image_path()).resize((100, 150)))
    top_card_label.config(image=card_image)
    top_card_label.image = card_image  # Keep a reference to avoid garbage collection
    current_card_name_label.config(text=f"Current Card: {top_card}")

def pc_turn():
    """Handles the PC's turn."""
    global top_card
    # Check if PC can play a card
    playable_card = None
    for idx, card in enumerate(pc_hand.cards):
        if single_card_check(top_card, card):
            playable_card = pc_hand.remove_card(idx)
            break
    if playable_card:
        top_card = playable_card
        update_top_card()
        update_pc_status()
        if win_check(pc_hand):
            messagebox.showinfo("UNO", "PC Won!")
            root.quit()
    else:
        # If no playable card, pull a card
        pc_hand.add_card(deck.deal())
        update_pc_status()

def update_pc_status():
    """Updates the PC's card count display."""
    pc_status_label.config(text=f"PC has {pc_hand.no_of_cards()} cards remaining")

# Game Setup
deck = Deck()
deck.shuffle()

player_hand = Hand()
pc_hand = Hand()

for _ in range(7):
    player_hand.add_card(deck.deal())
    pc_hand.add_card(deck.deal())

top_card = deck.deal()
while top_card.cardtype != 'number':
    top_card = deck.deal()

# GUI Setup
root = tk.Tk()
root.title("UNO Game")

# Top Card Frame
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

top_card_label = tk.Label(top_frame, text="Top Card", bg="white")
top_card_label.pack()

# Current Card Name
current_card_name_label = tk.Label(top_frame, text="Current Card: None", font=("Arial", 14))
current_card_name_label.pack()

# Player Hand Frame
player_frame = tk.Frame(root)
player_frame.pack(pady=10)

# Pull Button
pull_button = tk.Button(root, text="Pull Card", font=("Arial", 14), command=pull_card)
pull_button.pack(pady=5)

# PC Status Label
pc_status_label = tk.Label(root, text=f"PC has {pc_hand.no_of_cards()} cards remaining", font=("Arial", 16))
pc_status_label.pack(pady=5)

# Initial Updates
update_hand()
update_top_card()

# Mainloop
root.mainloop()
