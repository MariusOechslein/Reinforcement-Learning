from game import GamePlay
from learning_method import Strategy
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


# these are game variables, can skew them if you wish to
default_deck_content = ['A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', \
                      '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', \
                      '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', \
                      '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']

arbitrary_deck_content = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                        'A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', \
                      '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', \
                      '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', \
                      '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']

initial_number_of_card = 2
winning_points = 21
dealer_critical_points_to_stick = 17;

# train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table

#number_of_iterations = 10000000 # TODO: Intitial good results
num_iterations = 1000 # TODO: For less training time

QTableDictForQL = train_and_test_game_bot(num_iterations, 100000, "Q-Learning", default_deck_content, initial_number_of_card, winning_points, dealer_critical_points_to_stick)
QTableDictForSS = train_and_test_game_bot(num_iterations, 100000, "Sarsa", default_deck_content, initial_number_of_card, winning_points, dealer_critical_points_to_stick)
QTableDictForTD = train_and_test_game_bot(num_iterations, 100000, "Temporal Difference", default_deck_content, initial_number_of_card, winning_points, dealer_critical_points_to_stick)




### PRINTING
# lambda function for determine hit or stick
HitOrStick = lambda hitQ, stickQ: "H" if hitQ >= stickQ else "S"

# report strategy result
for i in range(0, winning_points*3-19):
    print(" ", end = "")
print("Q-learning", end = "")
print()

print("              player (usable ace)", end = " ")
for i in range(0, winning_points*3-36):
    print(" ", end="")
print("player (no usable ace)    ")

print("          ", end = "")
for p in range(11, winning_points+1):
    print(p, end = " ")
print("              ", end="")
for p in range(11, winning_points+1):
    print(p, end = " ")
print()

for d in range (1,11):
    if (d == 10):
        print("      10   ", end = "")
    elif (d == 3):
        print("    D  3   ", end = "")
    elif (d == 4):
        print("    e  4   ", end = "")
    elif (d == 5):
        print("    a  5   ", end = "")
    elif (d == 6):
        print("    l  6   ", end = "")
    elif (d == 7):
        print("    e  7   ", end = "")
    elif (d == 8):
        print("    r  8   ", end = "")
    else:
        print("      ", d, "  ", end = "")

    for p in range(11, winning_points+1):
        print(HitOrStick (QTableDictForQL[p,d,1,0], QTableDictForQL[p,d,1,1]), "", end = " ")

    if (d == 10):
        print("         10  ", end = " ")
    elif (d == 3):
        print("      D   3  ", end = " ")
    elif (d == 4):
        print("      e   4  ", end = " ")
    elif (d == 5):
        print("      a   5  ", end = " ")
    elif (d == 6):
        print("      l   6  ", end = " ")
    elif (d == 7):
        print("      e   7  ", end = " ")
    elif (d == 8):
        print("      r   8  ", end = " ")
    else:
        print("         ", d, " ", end = " ")

    for p in range(11, winning_points+1):
        print(HitOrStick (QTableDictForQL[p,d,0,0], QTableDictForQL[p,d,0,1]), "", end = " ")
    print()
print()




for i in range(0, winning_points*3-17):
    print(" ", end = "")
print("Sarsa", end = "")
print()

print("              player (usable ace)", end = " ")
for i in range(0, winning_points*3-36):
    print(" ", end="")
print("player (no usable ace)    ")

print("         ", end = " ")
for p in range(11, winning_points+1):
    print(p, end = " ")
print("             ", end=" ")
for p in range(11, winning_points+1):
    print(p, end = " ")
print()

for d in range (1,11):
    if (d == 10):
        print("      10   ", end = "")
    elif (d == 3):
        print("    D  3   ", end = "")
    elif (d == 4):
        print("    e  4   ", end = "")
    elif (d == 5):
        print("    a  5   ", end = "")
    elif (d == 6):
        print("    l  6   ", end = "")
    elif (d == 7):
        print("    e  7   ", end = "")
    elif (d == 8):
        print("    r  8   ", end = "")
    else:
        print("      ", d, "  ", end = "")

    for p in range(11, winning_points+1):
        print(HitOrStick (QTableDictForSS[p,d,1,0], QTableDictForSS[p,d,1,1]), "", end = " ")

    if (d == 10):
        print("         10  ", end = " ")
    elif (d == 3):
        print("      D   3  ", end = " ")
    elif (d == 4):
        print("      e   4  ", end = " ")
    elif (d == 5):
        print("      a   5  ", end = " ")
    elif (d == 6):
        print("      l   6  ", end = " ")
    elif (d == 7):
        print("      e   7  ", end = " ")
    elif (d == 8):
        print("      r   8  ", end = " ")
    else:
        print("         ", d, " ", end = " ")

    for p in range(11, winning_points+1):
        print(HitOrStick (QTableDictForSS[p,d,0,0], QTableDictForSS[p,d,0,1]), "", end = " ")

    print()
print()




for i in range(0, winning_points*3-23):
    print(" ", end = "")
print("Temporal Difference", end = "")
print()

print("              player (usable ace)", end = " ")
for i in range(0, winning_points*3-36):
    print(" ", end="")
print("player (no usable ace)    ")

print("         ", end = " ")
for p in range(11, winning_points+1):
    print(p, end = " ")
print("             ", end=" ")
for p in range(11, winning_points+1):
    print(p, end = " ")
print()

for d in range (1,11):
    if (d == 10):
        print("      10   ", end = "")
    elif (d == 3):
        print("    D  3   ", end = "")
    elif (d == 4):
        print("    e  4   ", end = "")
    elif (d == 5):
        print("    a  5   ", end = "")
    elif (d == 6):
        print("    l  6   ", end = "")
    elif (d == 7):
        print("    e  7   ", end = "")
    elif (d == 8):
        print("    r  8   ", end = "")
    else:
        print("      ", d, "  ", end = "")

    for p in range(11, winning_points+1):
        print(HitOrStick (QTableDictForTD[p,d,1,0], QTableDictForTD[p,d,1,1]), "", end = " ")

    if (d == 10):
        print("         10  ", end = " ")
    elif (d == 3):
        print("      D   3  ", end = " ")
    elif (d == 4):
        print("      e   4  ", end = " ")
    elif (d == 5):
        print("      a   5  ", end = " ")
    elif (d == 6):
        print("      l   6  ", end = " ")
    elif (d == 7):
        print("      e   7  ", end = " ")
    elif (d == 8):
        print("      r   8  ", end = " ")
    else:
        print("         ", d, " ", end = " ")

    for p in range(11, winning_points+1):
        print(HitOrStick (QTableDictForTD[p,d,0,0], QTableDictForTD[p,d,0,1]), "", end = " ")

    print()
