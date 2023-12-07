import csv
import random

# Load Q-table from CSV
Q_table = {}
with open('q_table.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        state = row[0]
        actions = list(map(float, row[1:]))
        Q_table[state] = actions


def get_possible_actions(state):
    return [i for i, x in enumerate(state) if x == 0]


def is_winner(state, player):
    winning_states = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(all(state[pos] == player for pos in combo) for combo in winning_states)


def update_state(state, action, player):
    new_state = state[:]
    new_state[action] = player
    return new_state


def play_game():
    state = [0] * 9  # Starting state - empty board
    game_log = []  # To log each move

    # Determine who starts: 1 for Player 1, 2 for Player 2
    if player_1_always_starts:
        current_player = 1
    else:
        current_player = 1 if random.random() < 0.5 else 2

    while True:
        game_log.append(state[:])  # Log current state
        state_str = str(state)
        actions = get_possible_actions(state)

        if not actions:  # No more actions possible
            return 0, game_log  # Draw

        if current_player == 1 and use_q_table:
            # Our agent's turn
            if state_str in Q_table:
                action = max(actions, key=lambda x: Q_table[state_str][x])
            else:
                action = random.choice(actions)  # Random move if state not in Q-table
        else:
            # Random player's turn
            action = random.choice(actions)

        state = update_state(state, action, current_player)
        if is_winner(state, current_player):
            return current_player, game_log

        current_player = 1 if current_player == 2 else 2  # Switch player


# Play 1000 games and track outcomes
num_games = 100000
wins = 0
draws = 0
losses = 0
log_lost_games = False
use_q_table = True
player_1_always_starts = False

if log_lost_games:
    # Open a file to log lost games only if flag is true
    log_file = open('lost_games_log.csv', 'w', newline='')
    log_writer = csv.writer(log_file)

for _ in range(num_games):
    result, game_log = play_game()
    if result == 1:  # Player 1 wins
        wins += 1
    elif result == 0:  # Draw
        draws += 1
    else:  # Player 2 wins
        losses += 1
        if log_lost_games:
            log_writer.writerows(game_log)  # Log the lost game

if log_lost_games:
    log_file.close()


print(f"Player 1 won: {wins} games")
print(f"Draws: {draws}")
print(f"Player 1 lost: {losses} games")
