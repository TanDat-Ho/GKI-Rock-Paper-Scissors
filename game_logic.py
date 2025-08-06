def determine_winner(p1_choice, p2_choice):
    """Determine winner logic"""
    if p1_choice == p2_choice:
        return 0  # Draw
    elif (p1_choice == 'rock' and p2_choice == 'scissors') or \
         (p1_choice == 'scissors' and p2_choice == 'paper') or \
         (p1_choice == 'paper' and p2_choice == 'rock'):
        return 1  # Player 1 wins
    else:
        return 2  # Player 2 wins
