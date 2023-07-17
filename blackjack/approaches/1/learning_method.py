from game import GamePlay
import random

class Strategy:

    def random_action(self):
        if random.random() <= 0.5:
            return 0
        else:
            return 1

    def epsilon_greedy_policy_from_q_table_dict(self, epsilon, q_table_dict, player_card_points, dealer_card_points, player_card_usable_ace):
        # P = epsilon: exploration
        if random.random() < epsilon:
            return self.random_action()
        # P = 1-epsilon: exploitation
        else:
            return self.best_action_policy_from_q_table_dict(q_table_dict, player_card_points, dealer_card_points, player_card_usable_ace)

    def best_action_policy_from_q_table_dict(self, q_table_dict, player_card_points, dealer_card_points, player_card_usable_ace):
        # Q function for state (playerCardPoints, dealerCardPoints, hit)
        hit_value = q_table_dict[(player_card_points, dealer_card_points, player_card_usable_ace, 0)]
        # Q function for state (playerCardPoints, dealerCardPoints, stick)
        stick_value = q_table_dict[(player_card_points, dealer_card_points, player_card_usable_ace, 1)]

        if hit_value > stick_value:
            return 0
        elif stick_value > hit_value:
            return 1
        else:
            return self.random_action()

    def update_q_table_dict(self, reward, occurred_state_actions, q_table_dict, state_count, state_action_count, method, gamma = 0.8):
        # update over all keys
        for i in range(len(occurred_state_actions)):
            state = occurred_state_actions[i][:-1]
            state_action = occurred_state_actions[i]
            # update counts
            state_count[state] += 1
            state_action_count[state_action] += 1

            # set the learning rate
            alpha = 1.0 / state_action_count[state_action]

            # update value function
            # for Q-learning or Sarsa
            if (method == "Q-Learning" or method == "Sarsa"):
                previous_Q = q_table_dict[state_action]
                # calculate the best Q value for (next state, best action)
                if i < len(occurred_state_actions) - 1:
                    # for Q-learning
                    if (method == "Q-Learning"):
                        next_state_hit_action = occurred_state_actions[i + 1][:-1] + (0,)
                        next_state_stick_action = occurred_state_actions[i + 1][:-1] + (1,)
                        maxvalue = max(q_table_dict[next_state_hit_action], q_table_dict[next_state_stick_action])
                        best_next_Q = gamma * maxvalue
                    # for Sarsa
                    else:
                        next_state_action = occurred_state_actions[i + 1]
                        best_next_Q = gamma * q_table_dict[next_state_action]
                else:
                    best_next_Q = 0

                # update the Q table dict
                q_table_dict[occurred_state_actions[i]] = (1 - alpha) * previous_Q + alpha * (reward + best_next_Q)

            # for Temporal Difference
            else:
                q_table_dict[occurred_state_actions[i]] += alpha * (reward - q_table_dict[occurred_state_actions[i]])

from collections import defaultdict
import sys

def train_and_test_game_bot(training_iteration, testing_iteration, method, deck_content, initial_number_of_card, \
                         winning_points, dealer_critical_points_to_stick):

    #check input parameter robustness
    if (initial_number_of_card * 10 > winning_points):
        print("initial card points can exceed the winning points, not allowed")
        sys.exit();

    if (initial_number_of_card < 1):
        print("initial number of card shall be equal ot greater than one")
        sys.exit();

    if (dealer_critical_points_to_stick > winning_points):
        print("dealer will hit until bust")
        sys.exit()

    # when player combats with dealer after the training phase,
    # this list stores the result [#win, #draw, #lose]
    test_result = [0, 0, 0];

    # dictionary: key = playerCardPoints, dealerFirstCardPoint, usableAce (no usable=0, has usable=1), action (hit=0, stick=1), value = Q function
    # this dict is the Q-table, stores rthe Q value for all combinations of states and actions
    q_table_dict = defaultdict(float)
    # dictionary: key = (playerCardPoints, dealerFirstCardPoint, usableAce (no usable=0, has usable=1)), value = number of occurrence throughout the iterations
    # this dict is used to determine epsilon (epsilon-greedy policy)
    state_count = defaultdict(int)
    # dictionary: key = (playerCardPoints, dealerFirstCardPoint, usableAce (no usable=0, has usable=1), action (hit=0, stick=1), value = number of occurrence throughout the iterations
    # this dict is used to determine alpha (learning rate)
    state_action_count = defaultdict(int)

    strategy = Strategy()

    for i in range(training_iteration + testing_iteration):

        # hit = 0, stick = 1
        action = None

        # if player wins dealer, reward = 1
        # if player draws dealer, reward = 0
        # if player loses dealer, reward = -1
        # used to update the Q function
        reward = None

        # start a game
        gameplay = GamePlay(deck_content, initial_number_of_card, winning_points)

        # a list stores the occurred key = playerCardPoints, dealerCardPoints, action (hit=0, stick=1)
        occurred_state_actions = []

        # start the game until it is finished
        while not gameplay.finish:

            # find an action defined by the policy map
            if action is not 1:
                # in training phase, use epsilon greedy policy
                if (i < training_iteration):
                    epsilon = 100 / float(100 + state_count[(gameplay.player_card_points, gameplay.dealer_first_card_point, gameplay.player_card_usable_ace)])
                    action = strategy.epsilon_greedy_policy_from_q_table_dict(epsilon, q_table_dict, gameplay.player_card_points, gameplay.dealer_first_card_point, gameplay.player_card_usable_ace)
                # in testing phase, use greedy policy
                else:
                    action = strategy.best_action_policy_from_q_table_dict(q_table_dict, gameplay.player_card_points, gameplay.dealer_first_card_point, gameplay.player_card_usable_ace)

            # if (playerCardPoints, dealerFirstCardPoint, action) is the newly occurred key
            # store this key for an update of Q-table in the end of this gameplay
            if (gameplay.player_card_points, gameplay.dealer_first_card_point, gameplay.player_card_usable_ace, action) not in occurred_state_actions and gameplay.player_card_points <= winning_points:
                occurred_state_actions.append((gameplay.player_card_points, gameplay.dealer_first_card_point, gameplay.player_card_usable_ace, action))

            # game proceed by the player's action
            # playerCardPoints, dealerCardPoints and reward will be updated
            [gameplay.player_card_points, gameplay.dealer_card_points, gameplay.player_card_usable_ace, reward] = gameplay.game_proceed(gameplay, action, winning_points, dealer_critical_points_to_stick)

            # game is finished if reward is out
            if (reward is not None):
                gameplay.finish = True

        # in training phase, use epsilon greedy policy, update the Q table dict
        if (i < training_iteration):
            strategy.update_q_table_dict(reward, occurred_state_actions, q_table_dict, state_count, state_action_count, method)
        # in testing phase, update the test result list
        else:
            if (reward == 1):
                test_result [0] += 1
            elif (reward == -1):
                test_result [2] += 1
            else:
                test_result [1] += 1

    print("After train for ", training_iteration, " iterations using", method)
    print("Our game bot fights against the dealer for ", testing_iteration, " rounds")
    print("Win: ", (float)(test_result [0])/testing_iteration*100.0, "%")
    print("Draw: ", (float)(test_result [1])/testing_iteration*100.0, "%")
    print("Lose: ", (float)(test_result [2])/testing_iteration*100.0, "%")
    print()

    return q_table_dict

