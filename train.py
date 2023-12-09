import random
import csv

# Parameters for Q-learning
learning_rate = 0.2
discount_factor = 0.9
num_episodes = int(1e7)
epsilon = 1.0  # Exploration rate
epsilon_min = 0.01
epsilon_decay = 0.999

# Initialise Q-table
Q_table = {}


def get_possible_actions(state):
    return [i for i, x in enumerate(state) if x == 0]


def is_winner(state, player):
    winning_states = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(all(state[pos] == player for pos in combo) for combo in winning_states)


def update_state(state, action, player):
    new_state = state[:]
    new_state[action] = player
    return new_state


def get_next_state_and_reward(state, action):
    new_state = update_state(state, action, 1)  # Player 1's move
    if is_winner(new_state, 1):
        return (new_state, 1)  # Reward for winning
    elif 0 not in new_state:
        return (new_state, 0.1)  # Draw
    else:
        # Player 2 (random) makes a move
        actions = get_possible_actions(new_state)
        random_action = random.choice(actions)
        new_state = update_state(new_state, random_action, 2)
        if is_winner(new_state, 2):
            return (new_state, -1)  # Penalty for losing
        else:
            return (new_state, 0)  # No immediate reward or penalty


# Q-learning algorithm
for episode in range(num_episodes):
    # if episode % (num_episodes // 10) == 0:
        # print(f"Episode {episode}")

    state = [0] * 9  # Starting state - empty board
    current_player = 1 if random.random() < 0.5 else 2

    # If Player 2 starts, make a random move
    if current_player == 2:
        actions = get_possible_actions(state)
        random_action = random.choice(actions)
        state = update_state(state, random_action, 2)
        current_player = 1  # Switch to Player 1

    while True:
        state_str = str(state)
        # add current state to Q table if it's not in there yet
        if state_str not in Q_table:
            Q_table[state_str] = [0] * 9

        actions = get_possible_actions(state)
        if not actions:  # No more actions possible
            break

        if random.uniform(0, 1) < epsilon:
            # Explore: choose a random action
            action = random.choice(actions)
        else:
            # Exploit: choose the best action based on Q-table
            action = max(actions, key=lambda x: Q_table[state_str][x])

        # Take action and observe new state and reward
        new_state, reward = get_next_state_and_reward(state, action)

        new_state_str = str(new_state)
        if new_state_str not in Q_table:
            Q_table[new_state_str] = [0] * 9

        Q_table[state_str][action] += learning_rate * (
                    reward + discount_factor * max(Q_table[new_state_str]) - Q_table[state_str][action])

        state = new_state

        if reward != 0:  # Game ended
            if reward == 1:
                player1_wins += 1
            elif reward == -1:
                player1_losses += 1
            else:
                player1_draws += 1
            break

    # Decay epsilon
    epsilon = max(epsilon_min, epsilon_decay * epsilon)

# Save Q-table to CSV file
with open('q_table.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for state, actions in Q_table.items():
        writer.writerow([state] + actions)

print("Q-table saved to q_table.csv")
