import random
import csv

# Board positions are indexed as follows:
# 0 | 1 | 2
# ---------
# 3 | 4 | 5
# ---------
# 6 | 7 | 8
#
# When prompted to make a move, enter the number corresponding to the position
# you want to play. For example, entering '0' will place your move in the top-left corner.


# Load Q-table from CSV file
Q_table = {}
with open('q_table.csv', mode='r') as file:
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


def transform_state_for_player2(state):
    return [2 if x == 1 else 1 if x == 2 else 0 for x in state]


def print_board(state):
    chars = {0: ' ', 1: 'X', 2: 'O'}
    for i in range(3):
        print(f"{chars[state[3 * i]]} | {chars[state[3 * i + 1]]} | {chars[state[3 * i + 2]]}")
        if i < 2:
            print("---------")


def get_agent_move(state, is_player1):
    if is_player1:
        state_str = str(state)
    else:
        transformed_state = transform_state_for_player2(state)
        state_str = str(transformed_state)

    if state_str not in Q_table:
        return random.choice(get_possible_actions(state))  # Random move if state not in Q-table
    return max(get_possible_actions(state), key=lambda x: Q_table[state_str][x])


def main():
    state = [0] * 9  # Starting state - empty board
    current_player = 1 if random.random() < 0.5 else 2

    while True:
        print_board(state)
        if current_player == 1:
            print("Your turn.")
            actions = get_possible_actions(state)
            move = int(input(f"Enter your move (0-8): "))
            while move not in actions:
                print("Invalid move. Try again.")
                move = int(input(f"Enter your move (0-8): "))
            state = update_state(state, move, 1)
        else:
            print("Agent's turn.")
            move = get_agent_move(state, is_player1=False)
            state = update_state(state, move, 2)

        if is_winner(state, current_player):
            print_board(state)
            if current_player == 1:
                print("You win!")
            else:
                print("Agent wins!")
            break
        elif 0 not in state:
            print_board(state)
            print("It's a draw!")
            break

        current_player = 1 if current_player == 2 else 2


if __name__ == "__main__":
    main()
