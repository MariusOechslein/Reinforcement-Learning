from learning_method import train_and_test_game_bot
from collections import defaultdict
import sys

# these are game variables, can skew them if you wish to
default_deck_content = ['A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', \
                      '4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', \
                      '7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', \
                      '10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']

#arbitrary_deck_content = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                        #'A', 'A', 'A', 'A', '2', '2', '2', '2', '3', '3', '3', '3', \
                      #'4', '4', '4', '4', '5', '5', '5', '5', '6', '6', '6', '6', \
                      #'7', '7', '7', '7', '8', '8', '8', '8', '9', '9', '9', '9', \
                      #'10', '10', '10', '10', 'J', 'J', 'J', 'J', 'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K']

initial_number_of_card = 2
winning_points = 21
dealer_critical_points_to_stick = 17;

# train agents using three different methods, (1) Q-learning (2) Sarsa (3) Temporal Difference, return Q table

#number_of_iterations = 10000000 # TODO: Intitial good results
num_iterations = 1000 # TODO: For less training time


### TODO: Specify here which methods to train with
#QTableDictForQL = train_and_test_game_bot(num_iterations, 100000, "Q-Learning", default_deck_content, initial_number_of_card, winning_points, dealer_critical_points_to_stick)
#QTableDictForSS = train_and_test_game_bot(num_iterations, 100000, "Sarsa", default_deck_content, initial_number_of_card, winning_points, dealer_critical_points_to_stick)
QTableDictForTD = train_and_test_game_bot(num_iterations, 100000, "Temporal Difference", default_deck_content, initial_number_of_card, winning_points, dealer_critical_points_to_stick)


### Plotting. With Matplotlib 3D plot or text output3D plot or text output
# TODO: Specify here whether to plot with matplotlib or with text output. Doing this since text output works in terminal and it will work forever, while matplotlib may change over time.
NEW_PLOTTING = False

if NEW_PLOTTING == True:
    import numpy as np
    from plotting import plot_blackjack_values
    from plotting import plot_policy

    # Value function
    plot_blackjack_values(QTableDictForQL)

    # Policy
    player_range = np.arange(11, 22)
    dealer_range = np.arange(10, 0, -1)
    policy = {}
    for x in player_range:
      for y in dealer_range:
        # for not usuable ace
        usuable_ace = 0
        val_hitting = QTableDictForQL[(x, y, usuable_ace, 1)]
        val_standing = QTableDictForQL[(x, y, usuable_ace, 0)]
        should_hit = int(val_hitting > val_standing)
        policy[(x, y, usuable_ace)] = should_hit

        # for usuable ace
        usuable_ace = 1
        val_hitting = QTableDictForQL[(x, y, usuable_ace, 1)]
        val_standing = QTableDictForQL[(x, y, usuable_ace, 0)]
        should_hit = int(val_hitting > val_standing)
        policy[(x, y, usuable_ace)] = should_hit

    plot_policy(policy) 

elif NEW_PLOTTING == False:
    ### PRINTING
    # lambda function for determine hit or stick
    HitOrStick = lambda hitQ, stickQ: "H" if hitQ >= stickQ else "-"

    try: 
        QTableDictForQL[15,5,1,0] # Try this line to see whether the Q-Table is initialized 

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
    except:
        # Don't print Q-learning
        pass




    try:
        QTableDictForSS[15,5,1,0] # Try this line to see whether the Q-Table is initialized 

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
    except:
        # Don't print SARSA
        pass



    try:
        QTableDictForTD[15,5,1,0] # Try this line to see whether the Q-Table is initialized 

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
    except:
        # Don't print Temporal Difference Learning
        pass


