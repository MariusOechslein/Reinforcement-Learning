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

